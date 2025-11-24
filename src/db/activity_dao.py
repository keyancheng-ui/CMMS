from db.validators import validate_date

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

    def add(self, manager_id, location_id, date_str, activity_type, description, requires_chemical=False):
        validate_date(date_str)
        cur = self.conn.cursor()
        cur.execute(
            "SELECT COUNT(1) FROM activities WHERE location_id=%s AND activity_date=%s",
            (location_id, date_str)
        )
        c = cur.fetchone()[0]
        if c and c > 0:
            cur.close()
            raise ValueError("location conflict")
        cur.execute(
            "INSERT INTO activities(manager_id, location_id, activity_date, activity_type, description, requires_chemical) VALUES(%s, %s, %s, %s, %s, %s)",
            (manager_id, location_id, date_str, activity_type, description, 1 if requires_chemical else 0)
        )
        self.conn.commit()
        cur.close()

    def assign_employee(self, activity_id, employee_id):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO activity_employees(activity_id, employee_id) VALUES(%s, %s)", (activity_id, employee_id))
        self.conn.commit()
        cur.close()

    def assign_contractor(self, activity_id, contractor_id):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO activity_contractors(activity_id, contractor_id) VALUES(%s, %s)", (activity_id, contractor_id))
        self.conn.commit()
        cur.close()

    def mark_complete(self, activity_id, result, finish_time):
        cur = self.conn.cursor()
        cur.execute("UPDATE activities SET result=%s, finish_time=%s WHERE id=%s", (result, finish_time, activity_id))
        self.conn.commit()
        cur.close()

    def list_by_filters(self, building=None, date_str=None, activity_type=None):
        sql = "SELECT a.id, a.activity_date, a.activity_type, a.description FROM activities a JOIN locations l ON a.location_id=l.id WHERE 1=1"
        vals = []
        if building:
            sql += " AND l.building=%s"; vals.append(building)
        if date_str:
            validate_date(date_str)
            sql += " AND a.activity_date=%s"; vals.append(date_str)
        if activity_type:
            sql += " AND a.activity_type=%s"; vals.append(activity_type)
        cur = self.conn.cursor(dictionary=True)
        cur.execute(sql, tuple(vals))
        rows = cur.fetchall()
        cur.close()
        return rows
