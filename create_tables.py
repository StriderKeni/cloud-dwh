import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries, table_list


def drop_tables(cur, conn):
    '''
    Function to drop all tables from Redshift Database
    Args:
        cur (object) = Cursor object from psycopg2 connection
        conn (object) = Connection to Amazon Redshift
        drop_table_queries (list) = List of drop table statements
        table_list (list) = List of all table names
    '''

    print('\n*** Dropping tables... ***\n')
    for query, table_name in zip(drop_table_queries, table_list):
        try:
            cur.execute(query)
            conn.commit()
            print('Table {} dropped succesfully'.format(table_name))
        except Exception as e:
            print(e)


def create_tables(cur, conn):
    '''
    Function to create all tables into Redshift
    Args:
        cur (object) = Cursor object from psycopg2 connection
        conn (object) = Connection to Amazon Redshift
        drop_table_queries (list) = List of drop table statements
        table_list (list) = List of all table names
    '''

    print('\n*** Creating tables... ***\n')
    for query, table_name in zip(create_table_queries, table_list):
        try:
            cur.execute(query)
            conn.commit()
            print("Table {} created succesfully".format(table_name))
        except Exception as e:
            print(e)


def main():

    # Initialize ConfigParser
    config = configparser.ConfigParser()
    # Read file with all information about AWS
    config.read('dwh.cfg')

    # Initialize connection
    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    # Cursor object
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
