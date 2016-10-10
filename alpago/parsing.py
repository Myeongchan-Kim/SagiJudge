# -*- coding: utf-8 -*-
import MySQLdb as mdb
from konlpy.tag import Twitter
from konlpy.tag import Kkma
from konlpy.utils import pprint
from threading import Thread
from more_itertools import unique_everseen
from collections import defaultdict, Counter
from os import listdir
from time import sleep
import cPickle as pickle
import operator
import jpype
import multiprocessing
import psutil
import sys
import math
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


def getMorphs(text):
    lines = convert_text_to_lines(text)
    sentences = do_sentencing_without_threading(lines)
    morphs_list = do_parsing_without_threading(sentences)
    s = defaultdict()
    for morphs in morphs_list:
        for morph in morphs:
            s.setdefault(morph[1], []).append(morph[0])
    return dict(s)

def analize_text(page_id, text):
    s = getMorphs(text)
    # with open('./pickles/dump_%d.pkl'%(post_id), 'w') as f:
        # morphs = pickle.dump(dict(s), f);
    save_tags(page_id, getCount(s))
    save_rate(page_id, s)
    return True


def getCount(dic):
    cnt = {}
    for key, val in dic.iteritems():
        if key == 'Noun':
            cnt = Counter(val)
    cnt = dict(cnt)
    sorted_cnt = sorted(cnt.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_cnt


def save_tags(page_id, lst):
    if not lst:
        return
    words = []
    count = 0
    for word, cnt in lst:
        if len(word) < 2:
            continue
        words.append(word)
        count += 1
        if count >= 5:
            break
    db = connect_db()
    cur = db.cursor()
    cur.executemany('insert ignore into tags (page_id, tag) values(%s, %s)',
                    map(lambda x: (page_id, x), words));
    db.commit()
    db.close()
    return True


def sigmoid(x):
      return 1 / (1 + math.exp(-x))

def score_eomi(lst):
    if not lst:
        return 0;
    eomi_total = len(lst)
    eomi_cnt = dict(Counter(lst))
    eomi_yo = 0
    if u'요' in eomi_cnt:
        eomi_yo += eomi_cnt[u'요']
    eomi_da = 0
    if u'다' in eomi_cnt:
        eomi_da += eomi_cnt[u'다']
    return sigmoid(eomi_da - eomi_yo)

def score_word(lst):
    neg_words = ['만병', '통치', '근원', '모든', '전부', '무조건', '절대',
             '꼭', '완전히', '안돼', '완전', '최고', '반드시', '암', '정화']
    pos_words = ['비교적', '안전', '낫다', '조직', '다소', '출처', '비판']

    if not lst:
        return 0;
    lst = filter(lambda x: (len(x) >= 2) || (x in neg_words || x in pos_words), lst)
    dic = dict(Counter(lst))
    neg_words = map(lambda x: u''+x, neg_words)
    neg_cnt = 0
    for word in neg_words:
        if word in dic:
            neg_cnt += dic[word]
    pos_words = map(lambda x: u''+x, pos_words)
    pos_cnt = 0
    for word in pos_words:
        if word in dic:
            pos_cnt += dic[word]
    print "pos_cnt: %d\t neg_cnt: %d\n" %(pos_cnt, neg_cnt)
    return sigmoid(pos_cnt - neg_cnt)

def get_rate(dic):
    lst = []
    val_word = 0
    val_eomi = 0
    for key, val in dic.iteritems():
        lst.extend(val)
    val_word = score_word(lst)
    # if 'Eomi' in dic:
        # val_eomi = score_eomi(dic['Eomi'])
    # return (val_word + v3al_eomi)/2
    return val_word

def save_rate(page_id, dic):
    rate = 100*get_rate(dic)
    if rate:
        db = connect_db()
        cur = db.cursor()
        cur.execute('insert into rates (user_id, page_id, rate) values (%s, %s, %s)',
                    (str(-1), str(page_id), str(rate)));
        db.commit()
        db.close()
    return True

def getById(id):
    db = connect_db()
    cur = db.cursor()
    cur.execute('select _id, content from pages where _id = %s', (str(id),))
    return cur.fetchall()[0][1]


def main():
    db = connect_db()
    cur = db.cursor()
    cur.execute('CALL getNewPages()')
    for row in cur.fetchall():
        page_id = row[0]
        content = row[1]
        print page_id
        if not content.strip(): continue
        print "Pageid(%d) started" % page_id
        analize_text(page_id, content)
    # db.close()


if __name__=='__main__':
    while(True):
        main()
        print 'done'
        sleep(60*20)
    # for filename in listdir('./pickles'):
        # if '.pkl' in filename:
            # with open('./pickles/'+filename, 'r') as f:
                # obj = pickle.load(f)
                # page_id = filename.split('.')[0].split('_')[1]
                # save_rate(page_id, obj)
                # save_tags(page_id, getCount(obj))
