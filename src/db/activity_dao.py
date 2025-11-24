class ActivityDAO:
    def __init__(self, conn):
        self.conn = conn

    def list_by_employee(self, employee_id):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            "SELECT id, description, activity_time FROM activities WHERE employee_id=%s",
            (employee_id,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def add(self, employee_id, description, activity_time):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO activities(employee_id, description, activity_time) VALUES(%s, %s, %s)",
            (employee_id, description, activity_time)
        )
        self.conn.commit()
        cur.close()
