import MySQLdb as mdb

mysql_info = dict(
    host = 'localhost',
    user = 'root',
    db = 'lacidem',
    charset = 'utf8'
)


def connect_db():
    conn = mdb.connect(**mysql_info)
    return conn


def init_db():
    db = connect_db()
    with open('./schema.sql') as f:
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
    db.close()


def main():
    print "initilizing tables..."
    init_db()
    print "DONE"


if __name__ == '__main__':
    main()
