import mysql.connector


class DatabaseConnection:
    def __init__(self, host='localhost', user='root', password='', database='appdb'):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )


    # general sql execution (CREATE)
    def execute_script(self, sql_script):
        cursor = self.connection.cursor()

        statements = sql_script.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        self.connection.commit() # write commands back to the database
        cursor.close()

    # execute query instruction (SELECT)
    def execute_query(self, query):
        cursor = self.connection.cursor(dictionary=True)

        statements = query.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        result = cursor.fetchall()
        cursor.close()
        return result

    # execute update instruction (UPDATE, INSERT, DELETE)
    def execute_update(self, query):
        cursor = self.connection.cursor()

        statements = query.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        self.connection.commit()
        result = cursor.rowcount
        cursor.close()
        return result

    def close(self):
        self.connection.close()