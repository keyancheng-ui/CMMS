class EmployeeDAO:
    def __init__(self, conn):
        self.conn = conn

    def list_all(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT id, name, role, location_id FROM employees")
        rows = cur.fetchall()
        cur.close()
        return rows

    def add(self, name, role, location_id=None):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO employees(name, role, location_id) VALUES(%s, %s, %s)",
            (name, role, location_id)
        )
        self.conn.commit()
        cur.close()
