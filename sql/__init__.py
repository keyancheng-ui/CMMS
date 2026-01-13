import os

# get sql file paths & define variables for these file paths
SQL_DIR = os.path.dirname(__file__)

SCHEMA_FILE = os.path.join(SQL_DIR, 'schema.sql')
TEST_DATA_FILE = os.path.join(SQL_DIR, 'test_data.sql')
SAMPLE_QUERIES_FILE = os.path.join(SQL_DIR, 'sample_queries.sql')

def get_schema():
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as file1:
        return file1.read()
def get_test_data():
    with open(TEST_DATA_FILE, 'r', encoding='utf-8') as file2:
        return file2.read()
def get_sample_queries():
    with open(SAMPLE_QUERIES_FILE, 'r', encoding='utf-8') as file3:
        return file3.read()

__all__ = ['get_schema', 'get_test_data', 'get_sample_queries']