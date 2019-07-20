''' package for connection to DB '''
import psycopg2
import sys
from configparser import ConfigParser
from psycopg2 import sql


def get_ini_file():
    '''read ini file for connection database'''
    config = ConfigParser()
    config.read(sys.path[0] + r'\database\db.ini')
    return config.get('db', 'db_name'),\
        config.get('db', 'db_user'),\
        config.get('db', 'db_password'),\
        config.get('db', 'db_location')


def is_check_db_instance(dbase, user_in, password_in, server):
    '''Is 'things' database instance?'''
    try:
        conn_ch = psycopg2.connect(user=user_in, password=password_in,
                                   host=server)
        cur = conn_ch.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname='{dbname}'".
                    format(dbname=dbase))
    except psycopg2.Error as e:
        print("No connect to server. Check logon/password in db.ini")
        exit()
    if cur.fetchone():
        cur.close()
        conn_ch.close()
        return True
    else:
        cur.close()
        conn_ch.close()
        return False


def create_db(dbase, user_in, password_in, server):
    ''' create new base if its new locate '''
    with open(sys.path[0]+r'\database\base.sql', 'r') as myfile:
        file_sql = myfile.read()
    script = file_sql.split(';')
    conn = psycopg2.connect(user=user_in, password=password_in, host=server)
    conn.autocommit = True
    cur = conn.cursor()
    print('Create database ' + dbase)
    cur.execute("CREATE DATABASE {}".format(dbase))
    cur.close()
    conn.close()
    conn = connect_to_db(dbase, user_in, password_in, server)
    conn.autocommit = True
    cur = conn.cursor()
    for string_sql in script:
        if len(string_sql.replace('\n', '')) > 0:
            print(string_sql.replace('\n', ''))
            cur.execute(string_sql.replace('\n', ''))
    cur.close()
    conn.close()


def connect_to_db(dbase, user_in, password_in, server):
    '''try to connect database'''
    try:
        conn = psycopg2.connect(dbname=dbase, user=user_in,
                                password=password_in, host=server)
    except psycopg2.ProgrammingError as e:
        print("Data base doesn`t exist!")
    return conn


def sql_result(conn, sql_text):
    with conn.cursor() as cursor:
        conn.autocommit = True
        sql_create = sql.SQL(sql_text)
        try:
            cursor.execute(sql_create)
            data = cursor.fetchall()
        except psycopg2.Error as e:
            return 0
        cursor.close()
        conn.close()
        return data


def is_sql_no_result(conn, sql_text):
    with conn.cursor() as cursor:
        conn.autocommit = True
        sql_create = sql.SQL(sql_text)
        try:
            cursor.execute(sql_create)
        except psycopg2.Error as e:
            return False
        cursor.close()
        conn.close()
        return True


if __name__ == "__main__":
    print(" This module not for running!")
