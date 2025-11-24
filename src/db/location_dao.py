class LocationDAO:
    def __init__(self, conn):
        self.conn = conn

    def list_all(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT id, building, floor, room FROM locations")
        rows = cur.fetchall()
        cur.close()
        return rows

    def add(self, building, floor, room):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO locations(building, floor, room) VALUES(%s, %s, %s)",
            (building, str(floor), str(room))
        )
        self.conn.commit()
        cur.close()

    def delete(self, location_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM locations WHERE id=%s", (location_id,))
        self.conn.commit()
        cur.close()
