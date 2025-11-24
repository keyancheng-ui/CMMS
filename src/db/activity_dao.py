from db.validators import validate_date

class ActivityDAO:
    def __init__(self, conn):
        self.conn = conn

    def list_by_employee(self, employee_ssn):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            "SELECT a.id, a.activity_date, a.activity_type, a.description FROM activities a JOIN activity_employees ae ON ae.activity_id=a.id WHERE ae.employee_ssn=%s",
            (employee_ssn,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def add(self, manager_id, location_id, date_str, activity_type, description, requires_chemical=False):
        validate_date(date_str)
        cur = self.conn.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM activity_locations al JOIN activities a ON a.id=al.activity_id WHERE al.location_id=%s AND a.activity_date=%s",
            (location_id, date_str)
        )
        c = cur.fetchone()[0]
        if c and c > 0:
            cur.close()
            raise ValueError("location conflict")
        cur.execute(
            "INSERT INTO activities(manager_id, activity_date, activity_type, description, requires_chemical) VALUES(%s, %s, %s, %s, %s)",
            (manager_id, date_str, activity_type, description, 1 if requires_chemical else 0)
        )
        aid = cur.lastrowid
        cur.execute(
            "INSERT INTO activity_locations(activity_id, location_id, reason) VALUES(%s, %s, %s)",
            (aid, location_id, "primary")
        )
        self.conn.commit()
        cur.close()

    def assign_employee(self, activity_id, employee_ssn):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO activity_employees(activity_id, employee_ssn) VALUES(%s, %s)", (activity_id, employee_ssn))
        self.conn.commit()
        cur.close()

    def assign_contractor(self, activity_id, contractor_id):
        raise NotImplementedError("Contractor assignments removed; use company-level supervision if needed")

    def mark_complete(self, activity_id, result, finish_time):
        cur = self.conn.cursor()
        cur.execute("UPDATE activities SET result=%s, finish_time=%s WHERE id=%s", (result, finish_time, activity_id))
        self.conn.commit()
        cur.close()

    def list_by_filters(self, building=None, date_str=None, activity_type=None):
        sql = "SELECT a.id, a.activity_date, a.activity_type, a.description FROM activities a JOIN activity_locations al ON al.activity_id=a.id JOIN locations l ON al.location_id=l.id WHERE 1=1"
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

    def unassign_employee(self, activity_id, employee_ssn):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM activity_employees WHERE activity_id=%s AND employee_ssn=%s", (activity_id, employee_ssn))
        self.conn.commit()
        cur.close()

    def unassign_contractor(self, activity_id, contractor_id):
        raise NotImplementedError("Contractor assignments removed; use company-level supervision if needed")

    def assign_temp_employee(self, activity_id, temp_employee_ssn):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO activity_temp_employees(activity_id, temp_employee_ssn) VALUES(%s, %s)", (activity_id, temp_employee_ssn))
        self.conn.commit()
        cur.close()

    def delete(self, activity_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM activity_employees WHERE activity_id=%s", (activity_id,))
        # contractors removed
        cur.execute("DELETE FROM activity_temp_employees WHERE activity_id=%s", (activity_id,))
        cur.execute("DELETE FROM activity_locations WHERE activity_id=%s", (activity_id,))
        cur.execute("DELETE FROM activities WHERE id=%s", (activity_id,))
        self.conn.commit()
        cur.close()

    def cleaning_schedule(self, building, start_date, end_date):
        validate_date(start_date)
        validate_date(end_date)
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT a.id AS activity_id, a.activity_date, a.description, a.requires_chemical,
                   CASE WHEN a.requires_chemical=1 THEN 1 ELSE 0 END AS unavailable,
                   l.building, l.floor, l.room
            FROM activities a
            JOIN activity_locations al ON al.activity_id=a.id
            JOIN locations l ON l.id=al.location_id
            WHERE a.activity_type='cleaning'
              AND l.building=%s
              AND a.activity_date BETWEEN %s AND %s
            ORDER BY a.activity_date ASC
            """,
            (building, start_date, end_date)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
