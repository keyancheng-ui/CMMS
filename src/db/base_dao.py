from .connection import DatabaseConnection


class BaseDAO:

    # connect to current database
    def __init__(self, db_connection, password):
        if db_connection is not None:
            # 如果传了现成的连接，直接用
            self.db = db_connection
        elif password is not None:
            # 如果传了密码，用它创建连接
            self.db = DatabaseConnection(password=password, database='appdb')
        else:
            # 都没传，才让用户输入
            pwd = input("Enter your own mySQL secret: (we are doing this then sth is wrong)")
            self.db = DatabaseConnection(password=pwd, database='appdb')

    # to execute query instruction
    def execute_query(self, query):
        return self.db.execute_query(query)

    # to execute update instruction
    def execute_update(self, query):
        return self.db.execute_update(query)

    # stop connection with the database
    def close(self):
        self.db.close()
