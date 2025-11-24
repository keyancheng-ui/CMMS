class EmployeeDAO:
    def __init__(self, conn):
        self.conn = conn

    def list_all(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT id, ssn, name, gender, level FROM employees")
        rows = cur.fetchall()
        cur.close()
        return rows

    def find_by_ssn(self, ssn):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT id, ssn, name, gender, level FROM employees WHERE ssn=%s", (ssn,))
        row = cur.fetchone()
        cur.close()
        return row

    def add(self, ssn, name, gender, level):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO employees(ssn, name, gender, level) VALUES(%s, %s, %s, %s)",
            (ssn, name, gender, level)
        )
        self.conn.commit()
        cur.close()

    def update(self, employee_id, name=None, gender=None, level=None):
        parts = []
        vals = []
        if name is not None:
            parts.append("name=%s"); vals.append(name)
        if gender is not None:
            parts.append("gender=%s"); vals.append(gender)
        if level is not None:
            parts.append("level=%s"); vals.append(level)
        if not parts:
            return
        sql = "UPDATE employees SET " + ", ".join(parts) + " WHERE id=%s"
        vals.append(employee_id)
        cur = self.conn.cursor()
        cur.execute(sql, tuple(vals))
        self.conn.commit()
        cur.close()

    def delete(self, employee_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
        self.conn.commit()
        cur.close()

    def set_supervisor(self, employee_id, supervisor_id):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE employees SET supervisor_id=%s WHERE id=%s",
            (supervisor_id, employee_id)
        )
        self.conn.commit()
        cur.close()
