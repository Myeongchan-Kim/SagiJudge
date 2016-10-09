# -*- coding: utf-8 -*-
import MySQLdb as mdb
from konlpy.tag import Twitter
from konlpy.tag import Kkma
from konlpy.utils import pprint
from threading import Thread
from more_itertools import unique_everseen
from collections import defaultdict, Counter
import cPickle as pickle
import operator
import jpype
import multiprocessing
import os
import psutil
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import imp
database_info = imp.load_source('database_info', '../database_info.py');
mysql_info = database_info.mysql_info


kkma = Kkma()
twitter = Twitter()

result_sentencing_thread = []
result_parsing_thread = []


def connect_db():
    db = mdb.connect(**mysql_info())
    return db


def convert_text_to_lines(text):
    if not text: return []
    lines = text.split('\n')
    ret = []
    for line in lines:
        line = u'%s' % line
        if line.strip() == '': continue
        ret.append(line)
    del lines
    return ret


def do_sentencing(start, end, lines, result_sentencing_thread):
    jpype.attachThreadToJVM()
    sentences = [kkma.sentences(lines[i]) for i in range(start, end)]
    result_sentencing_thread.append(sentences)
    return


def do_sentencing_by_threading(lines):
    nlines = len(lines)
    t1 = Thread(target=do_sentencing, args=(0, int(nlines/2), lines, result_sentencing_thread))
    t2 = Thread(target=do_sentencing, args=(int(nlines/2), nlines, lines, result_sentencing_thread))
    t1.start(); t2.start()
    t1.join(); t2.join()
    # jpype.detachThreadFromJVM()
    return sum(sum(result_sentencing_thread, []), [])


def do_sentencing_except_consonants(line):
    def is_consonant(c):
        return u'\u3130' < c < u'\u3164'
    start_consonant = []
    end_consonant = []
    for i in range(len(line)):
        c = line[i]
        if is_consonant(c):
            if i == 0:
               start_consonant.append(i)
            elif i == len(line)-1:
                end_consonant.append(i+1)
            elif not is_consonant(line[i-1]):
                start_consonant.append(i)
        else:
            if i != 0 and is_consonant(line[i-1]):
                end_consonant.append(i)
    consonant_cluster_index = zip(start_consonant, end_consonant)
    sentences = []

    if not consonant_cluster_index:
        sentences.extend(do_sentencing_line(line))
    else:
        start, end = consonant_cluster_index[0]
        if start != 0:
            sentences.extend(do_sentencing_line(line[0:start]))
        sentences.append(line[start:end])
        del consonant_cluster_index[0]
        prev = end
        for start, end in consonant_cluster_index:
            sentences.extend(do_sentencing_line(line[prev:start]))
            sentences.append(line[start:end])
            prev = end
        if prev != len(line):
            sentences.extend(do_sentencing_line(line[prev:]))
    return sentences


def do_sentencing_line(line):
    r_striped_line = line.rstrip()
    r_remainder = ''
    if len(line) != len(r_striped_line):
        r_remainder = line[len(r_striped_line):]

    l_striped_line = line.lstrip()
    l_remainder = ''
    if len(line) != len(l_striped_line):
        l_remainder = line[:len(line)-len(l_striped_line)]

    splited = line.split(' ')
    for i in range(len(splited)):
        chunk = splited[i]
        if len(chunk) > 20:
            print 'too long ', line
            return [line]

    sentences = []
    try:
        sentences.extend(kkma.sentences(line))
    except:
        print 'error ', line
        sentences.extend([line])

    sentences[-1] += r_remainder
    sentences[0] = l_remainder + sentences[0]

    return sentences


def do_sentencing_without_threading(lines):
    ret = []
    for line in lines:
        sentences = do_sentencing_except_consonants(line)
        ret.extend(sentences)
        del sentences[:]
    return ret


def do_parsing(start, end, sentences, result_parsing_thread):
    # jpype.attachThreadToJVM()
    morphs = [twitter.pos(sentences[i]) for i in range(start, end)]
    result_parsing_thread.append(morphs)
    return


def do_parsing_by_threading(sentences):
    nsentences = len(sentences)
    t1 = Thread(target=do_parsing, args=(0, int(nsentences/2), sentences, result_parsing_thread))
    t2 = Thread(target=do_parsing, args=(int(nsentences/2), nsentences, sentences, result_parsing_thread))
    t1.start(); t2.start()
    t1.join(); t2.join()
    # jpype.detachThreadFromJVM()
    return sum(result_parsing_thread, [])


def do_parsing_without_threading(sentences):
    if type(sentences) is list:
        return [twitter.pos(sentence) for sentence in sentences]
    else:
        jpype.attachThreadToJVM()
        return twitter.pos(sentences)


def dedup(l):
    return list(unique_everseen(l))


def concate_tuple(t):
    return '%s_%s' % t


def analize_text(post_id, text):
    lines = convert_text_to_lines(text)
    sentences = do_sentencing_without_threading(lines)
    morphs_list = do_parsing_without_threading(sentences)
    s = defaultdict()
    for morphs in morphs_list:
        for morph in morphs:
            s.setdefault(morph[1], []).append(morph[0])
    with open('./dump_%d.pkl'%(post_id), 'w') as f:
        morphs = pickle.dump(dict(s), f);

    cnt = {}
    for key, val in dict(s).iteritems():
        if key == 'Noun':
            cnt = Counter(val)
    cnt = dict(cnt)
    sorted_cnt = sorted(cnt.items(), key=operator.itemgetter(1), reverse=True)

    if sorted_cnt:
        return sorted_cnt[0:min(len(sorted_cnt), 5)]
    else:
        return None

def main():
    db = connect_db()
    cur = db.cursor()
    cur.execute('CALL getNewPages()')
    for row in cur.fetchall():
        post_id = row[0]
        content = row[1]
        pprint(analize_text(post_id, content))
    db.close()

if __name__=='__main__':
    main()
