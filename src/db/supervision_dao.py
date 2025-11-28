from .validators import ensure_distinct

class SupervisionDAO:
    def __init__(self, conn):
        self.conn = conn

    def set_supervision(self, employee_ssn, supervisor_ssn):
        ensure_distinct(employee_ssn, supervisor_ssn)
        cur = self.conn.cursor()
        cur.execute("UPDATE employees SET supervisor_ssn=%s WHERE ssn=%s", (supervisor_ssn, employee_ssn))
        self.conn.commit()
        cur.close()

    def list_subordinates(self, supervisor_ssn):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT ssn AS employee_ssn FROM employees WHERE supervisor_ssn=%s", (supervisor_ssn,))
        rows = cur.fetchall()
        cur.close()
        return rows

    def set_temp_supervision(self, temp_employee_ssn, supervisor_ssn):
        ensure_distinct(temp_employee_ssn, supervisor_ssn)
        cur = self.conn.cursor()
        cur.execute("DELETE FROM supervise_temp_employees WHERE temp_employee_ssn=%s", (temp_employee_ssn,))
        cur.execute(
            "INSERT INTO supervise_temp_employees(temp_employee_ssn, supervisor_ssn) VALUES(%s, %s)",
            (temp_employee_ssn, supervisor_ssn)
        )
        self.conn.commit()
        cur.close()

    def list_temp_subordinates(self, supervisor_ssn):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            "SELECT temp_employee_ssn FROM supervise_temp_employees WHERE supervisor_ssn=%s",
            (supervisor_ssn,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def set_contractor_company_supervision(self, company_name, supervisor_ssn):
        ensure_distinct(company_name, supervisor_ssn)
        cur = self.conn.cursor()
        cur.execute("DELETE FROM supervise_contractor_companies WHERE company_name=%s", (company_name,))
        cur.execute(
            "INSERT INTO supervise_contractor_companies(company_name, supervisor_ssn) VALUES(%s, %s)",
            (company_name, supervisor_ssn)
        )
        self.conn.commit()
        cur.close()

    def list_contractor_company_subordinates(self, supervisor_ssn):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            "SELECT company_name FROM supervise_contractor_companies WHERE supervisor_ssn=%s",
            (supervisor_ssn,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
