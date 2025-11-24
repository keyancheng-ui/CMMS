import os
from dotenv import load_dotenv
from mysql.connector import connect

load_dotenv()

def get_connection(pool_name: str = "app_pool", pool_size: int = 3):
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    database = os.getenv("MYSQL_DATABASE")
    return connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        pool_name=pool_name,
        pool_size=pool_size,
    )

def get_connection_no_db(pool_name: str = "init_pool", pool_size: int = 1):
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("MYSQL_USER") or os.getenv("MYSQL_ROOT_USER", "root")
    password = os.getenv("MYSQL_PASSWORD") or os.getenv("MYSQL_ROOT_PASSWORD")
    return connect(
        host=host,
        port=port,
        user=user,
        password=password,
        pool_name=pool_name,
        pool_size=pool_size,
    )

def ping():
    try:
        conn = get_connection()
    except Exception:
        host = os.getenv("MYSQL_HOST", "localhost")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        user = os.getenv("MYSQL_ROOT_USER", "root")
        password = os.getenv("MYSQL_ROOT_PASSWORD")
        database = os.getenv("MYSQL_DATABASE")
        conn = connect(host=host, port=port, user=user, password=password, database=database)
    cur = conn.cursor()
    cur.execute("SELECT 1")
    cur.fetchall()
    cur.close()
    conn.close()
