''' package for connection to DB '''
import psycopg2
from psycopg2 import sql


def is_check_db_password(dbase, user_in, password_in, server):
    '''Check user '''
    try:
        conn_ch = psycopg2.connect(dbname=dbase, user=user_in,
                                   password=password_in,
                                   host=server)
        cur = conn_ch.cursor()
    except psycopg2.OperationalError as e:
        return False
    cur.close()
    conn_ch.close()
    return True


def is_add_user(conn, user_in, password_in, role):
    with conn.cursor() as cursor:
        conn.autocommit = True
        try:
            if not role == 'SuperAdmin':
                sql_create = sql.SQL("CREATE USER {} WITH PASSWORD \
                                     '{}' INHERIT;".
                                     format(user_in, password_in))
            elif role == 'SuperAdmin':
                # PostgresSQL недавал нормально наследовать прова от роли
                # поэтому пришлось назначать права суперадмину непостредственно
                sql_create = sql.SQL("CREATE USER {} WITH PASSWORD \
                                     '{}' SUPERUSER CREATEROLE CREATEDB \
                                     INHERIT;GRANT ALL PRIVILEGES ON DATABASE \
                                     things TO {};".
                                     format(user_in, password_in, user_in))
            elif role == 'Admin':
                sql_create = sql.SQL("CREATE USER {} WITH PASSWORD \
                                     '{}' INHERIT;\
                                     GRANT ALL PRIVILEGES ON DATABASE \
                                     things TO {};".
                                     format(user_in, password_in, user_in))
            cursor.execute(sql_create)
            sql_create = sql.SQL('GRANT "{}" TO {};'.format(role, user_in))
            cursor.execute(sql_create)
        except psycopg2.Error as e:
            return False
        cursor.close()
        conn.close()
        return True


if __name__ == "__main__":
    print(" This module not for running!")
