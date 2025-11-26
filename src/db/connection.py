import mysql.connector
from mysql.connector import pooling
import os
from typing import Optional
import logging
import socket
import subprocess
import platform
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls, host: str = 'localhost', port: int = 3306, 
                       user: str = 'root', password: str = '', 
                       database: str = 'appdb', pool_size: int = 5):
        try:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name="appdb_pool",
                pool_size=pool_size,
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                autocommit=True,
                charset='utf8mb4'
            )
            logger.info("Database connection pool initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize database connection pool: {str(e)}")
            return False
    
    @classmethod
    def get_connection(cls):
        if cls._connection_pool is None:
            host = os.getenv('MYSQL_HOST', 'localhost')
            port = int(os.getenv('MYSQL_PORT', '3306'))
            user = os.getenv('MYSQL_USER', 'root')
            password = os.getenv('MYSQL_PASSWORD', '')
            database = os.getenv('MYSQL_DATABASE', 'appdb')
            cls._ensure_mysql_running(host, port)
            
            if not cls.initialize_pool(host, port, user, password, database):
                raise Exception("Database connection pool not initialized")
        
        try:
            connection = cls._connection_pool.get_connection()
            return connection
        except Exception as e:
            logger.error(f"Failed to get database connection: {str(e)}")
            raise
    
    @classmethod
    def get_connection_no_db(cls):
        try:
            connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                port=int(os.getenv('MYSQL_PORT', '3306')),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', ''),
                charset='utf8mb4'
            )
            return connection
        except Exception as e:
            logger.error(f"Failed to get database connection (no DB): {str(e)}")
            raise
    
    @classmethod
    def ping(cls) -> bool:
        try:
            connection = cls.get_connection()
            connection.ping(reconnect=True, attempts=3, delay=1)
            connection.close()
            logger.info("Database ping successful")
            return True
        except Exception as e:
            logger.error(f"Database ping failed: {str(e)}")
            return False

    @classmethod
    def _is_port_open(cls, host: str, port: int) -> bool:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except Exception:
            return False

    @classmethod
    def _start_mysql_service(cls, service_name: str) -> bool:
        try:
            if platform.system().lower() == 'windows':
                cmd = ["powershell", "-NoProfile", "-Command", f"Start-Service -Name '{service_name}'"]
                r = subprocess.run(cmd, capture_output=True, text=True)
                if r.returncode != 0:
                    cmd = ["cmd", "/c", f"net start \"{service_name}\""]
                    r = subprocess.run(cmd, capture_output=True, text=True)
                return r.returncode == 0
            return False
        except Exception:
            return False

    @classmethod
    def _ensure_mysql_running(cls, host: str, port: int):
        local_hosts = {'127.0.0.1', 'localhost'}
        if host.lower() not in local_hosts:
            return
        if cls._is_port_open(host, port):
            return
        svc = os.getenv('MYSQL_SERVICE_NAME') or ''
        candidates = [s for s in [svc, 'MySQL80', 'MySQL', 'mysql'] if s]
        for name in candidates:
            ok = cls._start_mysql_service(name)
            if ok:
                for _ in range(10):
                    if cls._is_port_open(host, port):
                        return
                    time.sleep(0.5)
        time.sleep(0.5)

def get_connection():
    return DatabaseConnection.get_connection()

def get_connection_no_db():
    return DatabaseConnection.get_connection_no_db()

def ping():
    return DatabaseConnection.ping()

def ping_server():
    host = os.getenv('MYSQL_HOST', 'localhost')
    port = int(os.getenv('MYSQL_PORT', '3306'))
    DatabaseConnection._ensure_mysql_running(host, port)
    try:
        conn = get_connection_no_db()
        conn.ping(reconnect=True, attempts=1, delay=0)
        conn.close()
        return True
    except Exception:
        return False
    
    @classmethod
    def bootstrap_database(cls):
        try:
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_file = os.path.join(current_dir, '../../sql/schema.sql')
            
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            sql_statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            
            connection = cls.get_connection_no_db()
            cursor = connection.cursor()
            
            for statement in sql_statements:
                if statement:
                    cursor.execute(statement)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info("Database bootstrap completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Database bootstrap failed: {str(e)}")
            return False
    
    @classmethod
    def initialize_with_data(cls, schema_file: str = None, data_file: str = None):
        try:
            if schema_file:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                
                connection = cls.get_connection()
                cursor = connection.cursor()
            
                for statement in schema_sql.split(';'):
                    if statement.strip():
                        cursor.execute(statement.strip())
                
                connection.commit()
                cursor.close()
                connection.close()
            
            if data_file:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data_sql = f.read()
                
                connection = cls.get_connection()
                cursor = connection.cursor()
                
                for statement in data_sql.split(';'):
                    if statement.strip():
                        cursor.execute(statement.strip())
                
                connection.commit()
                cursor.close()
                connection.close()
            
            logger.info("Database initialization with data completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            return False
