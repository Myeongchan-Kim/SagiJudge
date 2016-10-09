import MySQLdb as mdb
from database_info import mysql_info


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
                print query
                cursor.execute(query)
                print 'SUCCESS'
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
                print query
                cursor.execute(query)
                print 'SUCCESS'
                query = ''
            else:
                query += query_line
    db.close()

def main():
    print "initilizing tables..."
    # init_db('./schema.sql')
    # init_db('./dummy.sql')
    print "DONE"
    print "creating procedures..."
    create_proc()
    print "DONE"


if __name__ == '__main__':
    main()
