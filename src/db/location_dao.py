class LocationDAO:
    def __init__(self, conn):
        self.conn = conn

    def list_all(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT id, name FROM locations")
        rows = cur.fetchall()
        cur.close()
        return rows
