from .connection import DatabaseConnection


class BaseDAO:

    # connect to current database
    def __init__(self, db_connection=None):
        if db_connection:
            self.db = db_connection
        else:
            self.db = DatabaseConnection(database='appdb')

    # to execute query instruction
    def execute_query(self, query):
        return self.db.execute_query(query)

    # to execute update instruction
    def execute_update(self, query):
        return self.db.execute_update(query)

    # stop connection with the database
    def close(self):
        self.db.close()
