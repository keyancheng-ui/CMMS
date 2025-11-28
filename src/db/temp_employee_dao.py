from wsgiref.validate import validator

from .connection import DatabaseConnection
from .validators import Validators, ensure_not_empty
from .base_dao import BaseDAO

class TempEmployeeDAO(BaseDAO):

    def create_temp_employee(self, temp_ssn, company_name):
        ensure_not_empty(temp_ssn)
        ensure_not_empty(company_name)
        result = self.execute_query(
            f"SELECT * FROM Temporary_Employee WHERE Ssn = '{temp_ssn}'",
        )
        if(result.len==0):
            query = f"INSERT INTO Temporary_Employee (TempSsn, Company_name) VALUES ('{temp_ssn}', '{company_name}')"
            self.execute_update(query)
            print("Add new temporay employee: (ssn)",temp_ssn)
        else:
            print(f"Temporary employee {temp_ssn} exist.")

    def get_temp_employee_by_ssn(self, temp_ssn):
        ensure_not_empty(temp_ssn)
        query = f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'"
        result = self.execute_query(query)
        if result.len != 0:
            print("Get ",result[0]['TempSsn']," ",result[0]['Company_name'])
            return result
        else:
            print("There is not such temporary employee exist")
            return None


    def get_all_temp_employees(self):
        query = "SELECT * FROM Temporary_Employee ORDER BY Company_name, TempSsn"
        result = self.execute_query(query)
        if result.len != 0:
            for row in result:
                print(f"TempSsn: {row['TempSsn']}, Company_name: {row['Company_name']}")
            return result
        else:
            print("There is not temporary employee now")
            return None

    def delete_temp_employee(self, temp_ssn):
        ensure_not_empty(temp_ssn)
        
        check_query = f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'"
        result = self.execute_query(check_query)

        if len(result) == 0:
            print(f"Temporary employee {temp_ssn} does not exist.")
            return None

        delete_assignments_query = f"DELETE FROM Temp_Employee_Work_On WHERE Temp_Working_Worker_Ssn = '{temp_ssn}'"
        assignment_result = self.execute_update(delete_assignments_query)

        delete_employee_query = f"DELETE FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'"
        delete_result = self.execute_update(delete_employee_query)

        print(f"Deleted temporary employee: (ssn) {temp_ssn}")
        return delete_result


