from .base_dao import BaseDAO
from .validators import Validators


class SupervisionDAO(BaseDAO):

    # create new supervision if not exists
    def set_supervision(self, employee_ssn, supervisor_ssn):
        result1 = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{employee_ssn}'"
        )
        result2 = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{supervisor_ssn}'"
        )
        result3 = self.execute_query(
            f"SELECT * FROM Employee_Supervision WHERE Supervisor_Ssn = '{supervisor_ssn}' AND Supervisee_Ssn = '{employee_ssn}'"
        )

        if len(result1) != 0 and len(result2) != 0:
            if Validators.ensure_distinct(employee_ssn, supervisor_ssn):
                if len(result3) == 0:
                    level1 = result1[0]['Emp_Level']
                    level2 = result2[0]['Emp_Level']
                    if (level1 == 'base_level worker' and level2 == 'mid_level manager') or (level1 == 'base_level worker' and level2 == 'executive officer') or (level1 == 'mid_level manager' and level2 == 'executive officer'):
                        query = f"INSERT INTO Employee_Supervision (Supervisor_Ssn, Supervisee_Ssn) VALUES ('{supervisor_ssn}', '{employee_ssn}')"
                        return self.execute_update(query)
                    else:
                        print("Supervision is not qualified!")
                else:
                    print("Supervision already exists!")
            else:
                return
        else:
            print("Employee may not exist!")

    # list all supervision for an employee
    def list_supervision(self, ssn):
        result1 = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{ssn}'"
        )
        result2 = self.execute_query(
            f"SELECT * FROM Employee_Supervision WHERE Supervisor_Ssn = '{ssn}' OR Supervisee_Ssn = '{ssn}'"
        )
        if len(result1) != 0:
            if len(result2) != 0:
                for row in result2:
                    print(f"{row['Supervisor_Ssn']} supervises {row['Supervisee_Ssn']}")
            else:
                print("Supervision not exists! Set first!")
        else:
            print("Employee not exists!")

    def delete_supervision(self, supervisor_ssn, supervisee_ssn):
        result = self.execute_query(
            f"SELECT * FROM Employee_Supervision WHERE Supervisor_Ssn = '{supervisor_ssn}' AND Supervisee_Ssn = '{supervisee_ssn}'"
        )
        if len(result) > 0:
            query = f"DELETE FROM Employee_Supervision WHERE Supervisor_Ssn = '{supervisor_ssn}' AND Supervisee_Ssn = '{supervisee_ssn}'"
            self.execute_update(query)
        else:
            print("Supervision not exists!")

    # set a temp supervision
    def set_temp_supervision(self, temp_employee_ssn, supervisor_ssn):
        result1 = self.execute_query(
            f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_employee_ssn}'"
        )
        result2 = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{supervisor_ssn}'"
        )
        result3 = self.execute_query(
            f"SELECT * FROM TempSupervise WHERE Supervisor_Ssn_midlevel_manager = '{supervisor_ssn}' AND Supervisee_Ssn_temp_employee = '{temp_employee_ssn}'"
        )

        if len(result1) != 0 and len(result2) != 0:

            if len(result3) == 0:
                level2 = result2[0]['Emp_Level']
                if level2 == 'mid_level manager':
                    query = f"INSERT INTO TempSupervise (Supervisor_Ssn_midlevel_manager, Supervisee_Ssn_temp_employee) VALUES ('{supervisor_ssn}', '{temp_employee_ssn}')"
                    return self.execute_update(query)
                else:
                    print("Only middle level manager is qualified to supervise temp-workers!")
            else:
                print("Supervision already exists!")
        else:
            print("Employee may not exist!")

    # list the supervision of a temp-employee
    def list_temp_supervision(self, supervisee_ssn):
        result1 = self.execute_query(
            f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{supervisee_ssn}'"
        )
        result2 = self.execute_query(
            f"SELECT * FROM TempSupervise WHERE Supervisee_Ssn_temp_employee = '{supervisee_ssn}'"
        )
        if len(result1) != 0:
            if len(result2) != 0:
                for row in result2:
                    print(f"{row['Supervisor_Ssn_midlevel_manager']} supervises {row['Supervisee_Ssn_temp_employee']}")
            else:
                print("Supervision not exists! Set first!")
        else:
            print("Temp-employee not exists!")

    def delete_temp_supervision(self, temp_supervisee_ssn):
        result = self.execute_query(
            f"SELECT * FROM TempSupervise WHERE Supervisee_Ssn_temp_employee = '{temp_supervisee_ssn}'"
        )
        if len(result) > 0:
            query = f"DELETE FROM TempSupervise WHERE Supervisee_Ssn_temp_employee = '{temp_supervisee_ssn}'"
            self.execute_update(query)
        else:
            print("Supervision not exists!")

