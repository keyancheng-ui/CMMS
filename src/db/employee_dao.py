from .base_dao import BaseDAO


class EmployeeDAO(BaseDAO):

    def get_all_employees(self):
        return self.execute_query("SELECT * FROM Employee")

    def get_employee_by_ssn(self, ssn):
        result = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{ssn}'",
        )
        return result[0] if result else None

    def add_employee(self, ssn, name, emp_level):
        return self.execute_update(
            f"INSERT INTO Employee (Ssn, Name, Level) VALUES ('{ssn}', '{name}', '{emp_level}')",
        )

    def get_employees_by_level(self, level):
        return self.execute_query(
            f"SELECT * FROM Employee WHERE Level = '{level}'",
        )

    def update_employee(self, ssn, new_level):
        # check whether the employee exists
        result = self.get_employee_by_ssn(ssn)
        if len(result) > 0:
            query = f"UPDATE Employee SET Level = '{new_level}' WHERE Ssn = '{ssn}'"
            return self.execute_update(query)
        else:
            print("Employee not exists. Insert first.")
            name = input(f"Enter the name of employee {ssn}: ")
            self.add_employee(ssn, name, new_level)