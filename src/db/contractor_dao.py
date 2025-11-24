class ContractorDAO:
    def __init__(self, conn):
        self.conn = conn

    def add(self, ssn, name, company):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO contractors(ssn, name, company) VALUES(%s, %s, %s)", (ssn, name, company))
        self.conn.commit()
        cur.close()

    def list_all(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT id, ssn, name, company FROM contractors")
        rows = cur.fetchall()
        cur.close()
        return rows
