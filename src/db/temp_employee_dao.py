class TempEmployeeDAO:
    def __init__(self, conn):
        self.conn = conn

    def add(self, ssn, name, gender, company_id, supervisor_id):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO temp_employees(ssn, name, gender, company_id, supervisor_id) VALUES(%s, %s, %s, %s, %s)",
            (ssn, name, gender, company_id, supervisor_id)
        )
        self.conn.commit()
        cur.close()

    def list_all(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT id, ssn, name, gender, company_id, supervisor_id FROM temp_employees")
        rows = cur.fetchall()
        cur.close()
        return rows
