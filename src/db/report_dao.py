class ReportDAO:
    def __init__(self, conn):
        self.conn = conn

    def employee_activity_summary(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT e.id AS employee_id, e.name AS employee_name, COUNT(a.id) AS activity_count
            FROM employees e
            LEFT JOIN activities a ON a.employee_id = e.id
            GROUP BY e.id, e.name
            ORDER BY activity_count DESC
            """
        )
        rows = cur.fetchall()
        cur.close()
        return rows
