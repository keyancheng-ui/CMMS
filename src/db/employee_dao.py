from .base_dao import BaseDAO
from .validators import Validators


class EmployeeDAO(BaseDAO):

    # get all current standard employees in the database
    def get_all_employees(self):
        result = self.execute_query("SELECT * FROM Employee")
        for row in result:
            print(f"Ssn: {row['Ssn']}, Name: {row['Name']}, Level: {row['Emp_Level']}")

    # get an employee's name by its ssn
    def get_employee_by_ssn(self, ssn):
        result = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{ssn}'",
        )
        if len(result) > 0:
            print(result[0]['Name'])
        else:
            print(f"Employee {ssn} not exist. Insert first or check the input format.")

    # add new employees
    def add_employee(self, ssn, name, emp_level):
        if Validators.validate_employee_level(emp_level):
            result = self.execute_query(
                f"SELECT * FROM Employee WHERE Ssn = '{ssn}'",
            )
            if len(result) == 0:
                return self.execute_update(
                    f"INSERT INTO Employee (Ssn, Name, Emp_Level) VALUES ('{ssn}', '{name}', '{emp_level}')"
                )
            else:
                print("Employee already exist!")
        else:
            return

    # get employee by levels
    def get_employees_by_level(self, level):
        if Validators.validate_employee_level(level):
            result = self.execute_query(
                f"SELECT * FROM Employee WHERE Emp_Level = '{level}'",
            )
            for row in result:
                print(f"Ssn: {row['Ssn']}, Name: {row['Name']}, Level: {row['Emp_Level']}")
        else:
            return

    # promote an employee
    def update_employee(self, ssn, new_level):
        if Validators.validate_employee_level(new_level):
            result = self.execute_query(
                f"SELECT * FROM Employee WHERE Ssn = '{ssn}'",
            )
            if len(result) > 0:
                query = f"UPDATE Employee SET Emp_Level = '{new_level}' WHERE Ssn = '{ssn}'"
                return self.execute_update(query)
            else:
                print("Employee not exists. Insert first.")
                name = input(f"Enter the name of employee {ssn}: ")
                self.add_employee(ssn, name, new_level)
        else:
            return
