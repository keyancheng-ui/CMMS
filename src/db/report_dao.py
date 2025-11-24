class ReportDAO:
    def __init__(self, conn):
        self.conn = conn

    def employee_activity_summary(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT e.ssn AS employee_ssn, e.name AS employee_name, COUNT(ae.activity_id) AS activity_count
            FROM employees e
            LEFT JOIN activity_employees ae ON ae.employee_ssn = e.ssn
            GROUP BY e.ssn, e.name
            ORDER BY activity_count DESC
            """
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def activity_type_employee_count(self, start_date, end_date):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT a.activity_type AS type,
                   COUNT(DISTINCT ae.employee_id) AS employees,
                   COUNT(DISTINCT a.id) AS activities
            FROM activities a
            LEFT JOIN activity_employees ae ON ae.activity_id = a.id
            WHERE a.activity_date BETWEEN %s AND %s
            GROUP BY a.activity_type
            ORDER BY employees DESC
            """,
            (start_date, end_date)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def building_activity_status(self, building, start_date, end_date):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT l.building,
                   a.activity_type AS type,
                   COUNT(*) AS activity_count
            FROM activities a
            JOIN activity_locations al ON al.activity_id = a.id
            JOIN locations l ON l.id = al.location_id
            WHERE l.building = %s AND a.activity_date BETWEEN %s AND %s
            GROUP BY l.building, a.activity_type
            ORDER BY activity_count DESC
            """,
            (building, start_date, end_date)
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def chemical_usage(self, building, start_date, end_date):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT a.id AS activity_id, a.activity_date, a.description,
                   a.requires_chemical AS requires_chemical,
                   l.building, l.floor, l.room
            FROM activities a
            JOIN activity_locations al ON al.activity_id = a.id
            JOIN locations l ON l.id = al.location_id
            WHERE a.requires_chemical = 1
              AND l.building = %s
              AND a.activity_date BETWEEN %s AND %s
            ORDER BY a.activity_date ASC
            """,
            (building, start_date, end_date)
        )
        rows = cur.fetchall()
        cur.close()
        return rows
