import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, table_list


def load_staging_tables(cur, conn):
    '''
    Pipeline insert data into Redshift staging tables
    Args:
        cur (object) = Cursor object from psycopg2 connection
        conn (object) = Connection to Amazon Redshift
        copy_table_queries (list) = List of copy staging table statements
        table_list (list) = List of all table names
    '''

    for query, table_name in zip(copy_table_queries, table_list):
        print("\nLoading data to staging table {}".format(table_name))
        print("This process may take a moment. Please wait...")
        cur.execute(query)
        conn.commit()
        print("Data loaded succesfully to {}".format(table_name))


def insert_tables(cur, conn):
    '''
    Pipeline insert data into Redshift star-schema
    Args:
        cur (object) = Cursor object from psycopg2 connection
        conn (object) = Connection to Amazon Redshift
        insert_table_queries (list) = List of insert table statements
        table_list (list) = List of all table names, list starts from 2 because
                            the first elements are staging table names.
    '''

    for query, table_name in zip(insert_table_queries, table_list[2::]):
        print("\nInserting data into table {}".format(table_name))
        cur.execute(query)
        conn.commit()
        print("Data inserted succesfully into {}".format(table_name))


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

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
