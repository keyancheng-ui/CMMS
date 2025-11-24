class EmployeeDAO:
    def __init__(self, conn):
        self.conn = conn

    def list_all(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT ssn, name, level, supervisor_ssn, supervisee_ssn FROM employees")
        rows = cur.fetchall()
        cur.close()
        return rows

    def find_by_ssn(self, ssn):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT ssn, name, level, supervisor_ssn, supervisee_ssn FROM employees WHERE ssn=%s", (ssn,))
        row = cur.fetchone()
        cur.close()
        return row

    def add(self, ssn, name, level, supervisor_ssn=None, supervisee_ssn=None):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO employees(ssn, name, level, supervisor_ssn, supervisee_ssn) VALUES(%s, %s, %s, %s, %s)",
            (ssn, name, level, supervisor_ssn, supervisee_ssn)
        )
        self.conn.commit()
        cur.close()

    def update(self, employee_ssn, name=None, level=None, supervisor_ssn=None, supervisee_ssn=None):
        parts = []
        vals = []
        if name is not None:
            parts.append("name=%s"); vals.append(name)
        if level is not None:
            parts.append("level=%s"); vals.append(level)
        if supervisor_ssn is not None:
            parts.append("supervisor_ssn=%s"); vals.append(supervisor_ssn)
        if supervisee_ssn is not None:
            parts.append("supervisee_ssn=%s"); vals.append(supervisee_ssn)
        if not parts:
            return
        sql = "UPDATE employees SET " + ", ".join(parts) + " WHERE ssn=%s"
        vals.append(employee_ssn)
        cur = self.conn.cursor()
        cur.execute(sql, tuple(vals))
        self.conn.commit()
        cur.close()

    def delete(self, employee_ssn):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM employees WHERE ssn=%s", (employee_ssn,))
        self.conn.commit()
        cur.close()

    def set_supervisor(self, employee_ssn, supervisor_ssn):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE employees SET supervisor_ssn=%s WHERE ssn=%s",
            (supervisor_ssn, employee_ssn)
        )
        self.conn.commit()
        cur.close()
