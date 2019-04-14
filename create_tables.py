import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries, table_list


def drop_tables(cur, conn):

    print('\n*** Dropping tables... ***\n')
    for query, table_name in zip(drop_table_queries, table_list):
        try:
            cur.execute(query)
            conn.commit()
            print('Table {} dropped succesfully'.format(table_name))
        except Exception as e:
            print(e)


def create_tables(cur, conn):

    print('\n*** Creating tables... ***\n')
    for query, table_name in zip(create_table_queries, table_list):
        try:
            cur.execute(query)
            conn.commit()
            print("Table {} created succesfully".format(table_name))
        except Exception as e:
            print(e)


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
