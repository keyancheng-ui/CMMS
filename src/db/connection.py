import mysql.connector

class DatabaseConnection:
    def __init__(self, host='localhost', user='root', password='', database='appdb'):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def execute_script(self, sql_script):

        cursor = self.connection.cursor()
        statements = sql_script.split(';')

        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        self.connection.commit()
        cursor.close()
        print("sql script successfully executed")

    def close(self):
        self.connection.close()