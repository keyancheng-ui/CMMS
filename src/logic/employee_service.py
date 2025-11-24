class EmployeeService:
    def __init__(self, employee_dao):
        self.employee_dao = employee_dao

    def list_all(self):
        return self.employee_dao.list_all()
