class TempEmployeeDAO:
    def __init__(self, conn):
        self.conn = conn

    def add(self, ssn, name, company):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO temp_employees(TempSsn, name, company) VALUES(%s, %s, %s)",
            (ssn, name, company)
        )
        self.conn.commit()
        cur.close()

    def list_all(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT TempSsn AS ssn, name, company FROM temp_employees")
        rows = cur.fetchall()
        cur.close()
        return rows
