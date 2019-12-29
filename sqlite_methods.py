import sqlite3

location = 'data'
table_name = 'table_name'


def init():
    global conn
    global c
    conn = sqlite3.connect(location)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    create_database()


def create_database():
    sql = 'create table if not exists ' + table_name + ' (id integer)'
    c.execute(sql)
    conn.commit()


def create_database2():
    sql = 'create table ' + table_name + '(id integer)'
    c.execute(sql)
    conn.commit()


def clear_database():
    sql = 'drop table ' + table_name
    c.execute(sql)
    conn.commit()


def remake():
    clear_database()
    create_database()  # Replacing this with create_database2() works every time
    insert_record(1)
    conn.commit()


def insert_record(id):
    sql = 'insert into ' + table_name + ' (id) values (%d)' % (id)
    c.execute(sql)
    print('Inserted ', id)


def insert_row(conn, table, row):
    c = conn.cursor()
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    c.execute(sql, row)
    conn.commit()


def insert_many(conn, table, data):
    c = conn.cursor()
    for d in data:
        row = dict(
            id=d['id'],
            timestamp=d['timestamp'],
            amount=d['amount'],
            cost=d['cost'],
            price=d['price'],
            side=d['side'])
        cols = ', '.join('"{}"'.format(col) for col in row.keys())
        vals = ', '.join(':{}'.format(col) for col in row.keys())
        sql = 'INSERT OR IGNORE INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
        c.execute(sql, row)
    conn.commit()

# " VALUES ({','.join('?' * len(data[0]))})", data

# init()
# remake()
