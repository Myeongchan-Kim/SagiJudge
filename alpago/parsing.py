# -*- coding: utf-8 -*-
import MySQLdb as mdb
from konlpy.tag import Twitter
from konlpy.tag import Kkma
from konlpy.utils import pprint
from threading import Thread
from more_itertools import unique_everseen
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
    jpype.attachThreadToJVM()
    morphs = [twitter.morphs(sentences[i]) for i in range(start, end)]
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


def analize_text(text):
    lines = conver_text_to_lines(text)
    sentences = do_sentencing_by_threading(lines)
    morphs = do_parsing_by_threading(sentences)
    return morphs

def main():
    db = connect_db()
    cur = db.cursor()
    cur.execute('CALL getNewPages()')
    for row in cur.fetchall():
        post_id = row[0]
        content = row[1]
        analize_text(content)
    db.close()

if __name__=='__main__':
    text = """




대부분의 주류 의사들은 백신을 의학이 이뤄낸 위대한 업적으로 생각하며,
이것으로 여러 가지 감염성 질병을 몰아낼 수 있을 것으로 믿는 다.
소아마비뿐만 아니라 홍역, 볼거리, 수두 같은 아동기에 누구나 앓고 지나가는 가벼운 질병에 대해서도 공포를 과장하여 예방 접종을 남발하는 배경에는 의사들의 질병에 대한 무지와 약물에 대한 믿음,
그리고 돈에 대한 끝없는 탐욕이 자리 잡고 있다.

그러나 면력력을 이해하지 못하는 주류 의사들에 의해 우리나라에서는 태어나면서부터 초등학교 입학 전까지 접종해야 할 필수 예 방 접종이 9가지에 달하며, 접종 횟수는 무려 20회를 넘는다.
약물을 포함해 현대의학을 가장 신성시하는 미국은 12가지(호주, 캐나다도 동일),
일본은 6가지, 프랑스는 9가지에 달한다.
특히 미국은 초등학교에 입학하려면 12가지 백신을 모두 접종했음을 증명해야 한다.
그리고 만 18세가 될 때까지 40가지 이상의 백신 접종을 해야 한다.
전통 의학에 신뢰가 강한 독일과 프랑스는 의무 사항이 아니고 접종 여부를 선택할 권리가 부모에게 주어진다.

미국에서 생후 1년 이내에 접종하는 백신이 늘어나면서 1997년 이전에는 영아사망률이 세계 22위에서 천연두 백신 접종을 강제로  실시한 1997년 이후 34위로 급등했다.
매년 53,000여 명의 신생아가 출생 후 원인을 모른 채 죽어가고 있다.
부검 결과 사망원인을 찾아내지 못하는 경우에는 모두 유아돌연사(SIDS)라는 결론을 내리며 그 원인을 대부분 부모의 흡연 또는 침대에 엎드려 잠을 자다가 질식사한 것으로 결론을 내린다.
그러나 중요한 사실은 유아돌연사의 90%는 백신 접종이 집중되는 시기인 생후 6개월 이전의 유아에게 발생하며 게다가 미국에 백신이 도입되던 1950년대 이전에는 SIDS가 존재하지 않았다는 것이다.
백신 도입 초기인 1953년에는 1,000명당 2.5명의 SIDS가 발생한 반면 1992년에는 1,000명당 17.9명으로 증가했다.
일본은 유아 백신 접종 연령을 출생 후 2개월부터 2년 사이로 상향 조정함으로 SIDS 비율을 크게 떨어뜨렸다.

백신은 복제가 불가능하고, 백신 접종은 집단적으로 행해지며, 국가가 세금으로 지원하기 때문에 백신시장은 제약회사에 있어서는 안정적인 황금시장이다.
그렇기 때문에 제약회사는 백신 개발에 전력을 기울인다. 자궁경부암 백신뿐만 아니라 임신 예방 백신 등 지금까지 개발된 백신은 100여 가지에 해당한다.
현재는 백신용 바이러스를 유전자를 조작한 동식물에서 생산하는 연구를 진행 중이다.그러나 백신도 다른 의약품과 같이 심각한 부작용이 계속해서 보고되고 있다.
아직 성숙되지 않은 아동들의 면역 체계속으로 8가지 이상의 항원을 투입할 때 나타날 위험성에 대해서 주류 의사들은 거의 신경을 쓰지 않는다.
영국의 공중보건서비스의 연구 결과 홍역, 볼거리, 풍진9보통 이 세 가지 에방 접종은 한 번에 실시한다. (MMR이라고 한다) 예방  백신을 접종한 아동들이 접종하지 않은 다동들에 비해 근육 경련이 발생할 위험성이 세배나 높다고 한다.
그리고 간질의 경우는 거의 70%에 해당하는 경우가 홍역 백신에 의한 것으로 밝혀졌다.
또한 MMR 백신이 어린이의 면역 체계를 파괴해 백혈병을 유발하기도 한다.

반면 바이러스는 변이가 쉽게 이뤄지기 때문에 새롭게 변이된 바이러스에 대해서는 백신으로 형성된 약한 면역 체계가 제대로 대응하지 못할 수도 있다.
그리고 대부분의 나라에서 백신 접종 후에 발병하는 자폐증과 간질환이 백신 부작용으로 인한 소송에서 가장 큰 비중을 차지한다.
한편 의사인 바트 크레센에 의하면 제1형 당뇨병을 앓는 아동의 79%는 백신의 부작용 때문이라고 한다. 우울증 치료제인 자이프렉 사 등과 같은 약의 부작용까지 합친다면 당뇨병의 거의 대부분은 약의 부작용으로 인한 것이다.
그러나 이런 부작용에 대해서는 주류 의사와 주류 언론에 의해 철저히 숨겨진다.
이에 대해 미국국립보건원(NIH)의 바이러스 전문가인 앤소니 모리스는 “우리는 뇌염에 의한 사망 소식만 접하고 백신에 의한 사망 등 부작용에 대해서는 철저히 숨겨진다”고 지적한다.

거대 제약회사인 와이어스사의 자회사인 웨스 레들러사는 유아에게 위장염을 일으켜 설사를 유발시키는 원인으로 알려진 로타바이 러스에 대해 서전에 면역력을 향상시킬 수 있다는 이유로 로타실드라는 백신을 개발했다.
이 백신은 임상 시험 결과 안전성이 입증됐다며 생후 2, 4, 6개월 단위로 3번을 복용하면 평생 면역력이 생겨 로타바이러스로부터 80% 정도 해방된다고 선전했던 제품이다.
그러나 로타실드는 1998년 8월에 FDA의 승인을 받고 시판되다가 100건 이상의 심각한 장폐색 부작용이 확인되어 1년 만인 1999년 8월에 승인이 취소되고 시장에서 퇴출됐다. 후에 밝혀진 사실은 이 약의 승인 과정에서 FDA의 심사위원 5명 중 3명이 웨스 레들러사의 임원 또는 주주였고, 특히 1명은 로타실드의 특허권 보유자였다.

탐욕에 젖은 그들은 어린이들의 건강보다는 황금탑에 눈이 일그러져 심의 과정을 로비와 협박으로 비틀고 통과시킨 것이다.
중요한 사실은 장폐색으로 사망하거나 장애자가 된 어린이들 중 공식적으로 로타실드가 원인이라는 것이 확인된 사례만이 100여 건이고, 확인 안 된 사례까지 합한다면 수십만 명이 넘을 수도 있다는 것이다.
이후 와이어스사는 2008년 로타실드의 상품명을 로타릭스로 바꿔 다시 승인을 받고 현재 전 세계에서 시판 중이다.


"""
    morphs = analize_text(text)
    pprint(morphs)
