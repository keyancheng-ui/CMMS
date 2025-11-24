class TempEmployeeService:
    def __init__(self, dao):
        self.dao = dao

    def add(self, ssn, name, gender, company_id, supervisor_id):
        return self.dao.add(ssn, name, gender, company_id, supervisor_id)

    def list_all(self):
        return self.dao.list_all()
