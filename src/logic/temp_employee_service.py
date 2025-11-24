class TempEmployeeService:
    def __init__(self, dao):
        self.dao = dao

    def add(self, ssn, name, company):
        return self.dao.add(ssn, name, company)

    def list_all(self):
        return self.dao.list_all()
