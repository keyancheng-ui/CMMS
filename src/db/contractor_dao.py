class ContractorDAO:
    def __init__(self, conn):
        self.conn = conn

    def add(self, name):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO contractor_companies(name) VALUES(%s)", (name,))
        self.conn.commit()
        cur.close()

    def list_all(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT name FROM contractor_companies")
        rows = cur.fetchall()
        cur.close()
        return rows
