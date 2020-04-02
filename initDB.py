import MySQLdb as mdb
from database_info import mysql_info
from random import random


def connect_db():
    conn = mdb.connect(**mysql_info())
    return conn


def init_db(sql):
    db = connect_db()
    with open(sql) as f:
        cursor = db.cursor()
        query = ''
        while(True):
            query_line = f.readline()
            if not query_line:
                break
            query += query_line
            if ';' in query:
                print(query)
                cursor.execute(query)
                print('SUCCESS')
                query = ''
    db.commit()
    db.close()


# def create_proc():
    # db = connect_db()
    # with open('./procedure.sql') as f:
        # cursor = db.cursor()
        # query = ''
        # while(True):
            # query_line = f.readline()
            # if not query_line:
                # break
            # query += query_line
            # if ';' in query or '$$' in query:
                # cursor.execute(query)
                # print 'SUCCESS'
                # query = ''
    # db.close()

def create_proc():
    db = connect_db()
    with open('./procedure.sql') as f:
        cursor = db.cursor()
        query = ''
        while(True):
            query_line = f.readline()
            if not query_line:
                break;
            if '--' in query_line:
                print(query)
                cursor.execute(query)
                print('SUCCESS')
                query = ''
            else:
                query += query_line
    db.close()

def genDummy():
    db = connect_db()
    cur = db.cursor()
    page_idx = [1,2,3,4,5,6,7,10,13,14,15,16,17,18,19]
    for x in range(1000):
        user_id = int(random()*11 + 1)
        page_id = page_idx[int(random()*len(page_idx))]
        cur.execute('insert into rates (user_id, page_id, rate) values (%s, %s, %s)',
                    (str(user_id), str(page_id), str(int(random()*2))))
    db.commit()
    db.close()

def main():
    print("initilizing tables...")
    init_db('./schema.sql')
    init_db('./dummy.sql')
    print("DONE")
    print("creating procedures...")
    create_proc()
    print("DONE")
    # genDummy()
    print("dummyGen")


if __name__ == '__main__':
    main()
