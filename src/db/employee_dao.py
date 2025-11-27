from .base_dao import BaseDAO
from .validators import Validators


class EmployeeDAO(BaseDAO):

    def get_all_employees(self):
        result = self.execute_query("SELECT * FROM Employee")
        for tuple in result:
            print(f"Ssn: {tuple[0]}, Name: {tuple[1]}, Level: {tuple[2]}")

    def get_employee_by_ssn(self, ssn):
        result = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{ssn}'",
        )
        if len(result) > 0:
            return result[0]
        else:
            print(f"Employee {ssn} not exist. Insert first or check the input format.")
            return result

    def add_employee(self, ssn, name, emp_level):
        if Validators.validate_employee_level(emp_level):
            if len(self.get_employee_by_ssn(ssn)) == 0:
                return self.execute_update(
                    f"INSERT INTO Employee (Ssn, Name, Level) VALUES ('{ssn}', '{name}', '{emp_level}')"
                )
            else:
                print("Employee already exist!")
        else:
            return Validators.validate_employee_level(emp_level)

    def get_employees_by_level(self, level):
        if Validators.validate_employee_level(level):
            result = self.execute_query(
                f"SELECT * FROM Employee WHERE Level = '{level}'",
            )
            for row in result:
                print(f"Ssn: {row[0]}, Name: {row[1]}, Level: {row[2]}")
        else:
            return Validators.validate_employee_level(level)

    def update_employee(self, ssn, new_level):
        # check whether the level is qualified
        if Validators.validate_employee_level(new_level):
            # check whether the employee exists
            result = self.get_employee_by_ssn(ssn)
            if len(result) > 0:
                query = f"UPDATE Employee SET Level = '{new_level}' WHERE Ssn = '{ssn}'"
                return self.execute_update(query)
            else:
                print("Employee not exists. Insert first.")
                name = input(f"Enter the name of employee {ssn}: ")
                self.add_employee(ssn, name, new_level)
        else:
            return Validators.validate_employee_level(new_level)