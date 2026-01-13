from .connection import DatabaseConnection


class BaseDAO:

    # connect to current database
    def __init__(self, password=None):
       self.db = DatabaseConnection(password=password, database='appdb')

    # to execute query instruction
    def execute_query(self, query):
        return self.db.execute_query(query)

    # to execute update instruction
    def execute_update(self, query):
        return self.db.execute_update(query)

    # stop connection with the database
    def close(self):
        self.db.close()