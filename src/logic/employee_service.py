from src.db.employee_dao import EmployeeDAO
from src.db.location_dao import LocationDAO


class EmployeeService:
    # initialize the class and set needed objects
    def __init__(self):
        self.employee_dao = EmployeeDAO()
        self.location_dao = LocationDAO()

    # register employee from the user-service level
    def register_employee(self, ssn, name, level):
        self.employee_dao.add_employee(ssn, name, level)

    # get an employee by ssn from the user-service level
    def get_employee_by_ssn(self, ssn):
        self.employee_dao.get_employee_by_ssn(ssn)

    # get all employees from the user-service level
    def get_current_employee(self):
        self.employee_dao.get_all_employees()

    # get employees by their level
    def fetch_employee_by_level(self, level):
        self.employee_dao.get_employees_by_level(level)

    # promote an employee
    def employee_promotion(self, ssn, level):
        self.employee_dao.update_employee(ssn, level)





    def close(self):
        self.employee_dao.close()
