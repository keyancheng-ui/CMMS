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

    # execute query instruction (SELECT)
    def execute_query(self, query):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        self.connection.commit()
        result = cursor.fetchall()
        cursor.close()
        return result

    # execute update instruction (UPDATE, INSERT, DELETE)
    def execute_update(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        result = cursor.rowcount
        cursor.close()
        return result

    def close(self):
        self.connection.close()