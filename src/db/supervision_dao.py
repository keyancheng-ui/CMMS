from db.validators import ensure_distinct

class SupervisionDAO:
    def __init__(self, conn):
        self.conn = conn

    def set_supervision(self, employee_id, supervisor_id):
        ensure_distinct(employee_id, supervisor_id)
        cur = self.conn.cursor()
        cur.execute("INSERT INTO supervise(employee_id, supervisor_id) VALUES(%s, %s)", (employee_id, supervisor_id))
        self.conn.commit()
        cur.close()

    def list_subordinates(self, supervisor_id):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT employee_id FROM supervise WHERE supervisor_id=%s", (supervisor_id,))
        rows = cur.fetchall()
        cur.close()
        return rows
