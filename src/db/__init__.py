# connect database and import DAO classes
from .connection import DatabaseConnection

from .validators import *
from .quick_query_dao import QuickQueryDAO

import os

def read_sql_file(file_name):
    # find sql directory path
    current_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(os.path.dirname(current_dir))
    sql_dir = os.path.join(project_root, 'sql')

    sql_file_path = os.path.join(sql_dir, file_name)

    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error：cannot find file {sql_file_path}")
        return None

def get_database_schema():
    return read_sql_file('schema.sql')

def get_test_data():
    return read_sql_file('test_data.sql')

def get_sample_queries():
    return read_sql_file('sample_queries.sql')

# a function to initialize database
def initialize_database(host='localhost', user='root', password='', database='appdb'):

    try:
        # connect to mysql database
        db_system = DatabaseConnection(host=host, user=user, password=password, database='mysql')

        # create aiming database if not exist
        db_system.execute_script(f"CREATE DATABASE IF NOT EXISTS {database}")

        db_system.close()

        # connect to aiming database
        db = DatabaseConnection(host=host, user=user, password=password, database=database)

        schema_sql = get_database_schema()
        if schema_sql:
            db.execute_script(schema_sql)
            print("database successfully set")

        test_sql = get_test_data()
        if test_sql:
            db.execute_script(test_sql)
            print("test data successfully inserted")

        db.close()

    except Exception as e:
        print(f"database initialization failed: {e}")

__all__ = [
    'DatabaseConnection',
    'QuickQueryDAO',
    'get_database_schema',
    'get_test_data',
    'initialize_database'
]