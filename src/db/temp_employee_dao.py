from wsgiref.validate import validator

from .connection import DatabaseConnection
from .validators import Validators, ensure_not_empty
from .base_dao import BaseDAO


class TempEmployeeDAO(BaseDAO):

    def create_temp_employee(self, temp_ssn, company_name):
        ensure_not_empty(temp_ssn)
        ensure_not_empty(company_name)
        result = self.execute_query(
            f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'",
        )
        if len(result) == 0:
            query = f"INSERT INTO Temporary_Employee (TempSsn, Company_name) VALUES ('{temp_ssn}', '{company_name}')"
            print("Add new temporay employee: (ssn)", temp_ssn)
            return self.execute_update(query)
        else:
            print(f"Temporary employee {temp_ssn} exist.")
            return {"success": False, "error": "Temporary employee already exists"}

    def create_temp_employee_with_company(self, temp_ssn, company_name, contractor_company_name):
        ensure_not_empty(temp_ssn)
        ensure_not_empty(company_name)
        ensure_not_empty(contractor_company_name)

        result = self.execute_query(
            f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'",
        )

        if len(result) > 0:
            print(f"Temporary employee {temp_ssn} already exists.")
            return {"success": False, "error": "Temporary employee already exists"}

        query = f"INSERT INTO Temporary_Employee (TempSsn, Company_name) VALUES ('{temp_ssn}', '{company_name}')"
        employee_result = self.execute_update(query)
        print("Add new temporary employee: (ssn)", temp_ssn)

        contractor_query = f"INSERT INTO Contractor_Company (name, Temp_Employee_Ssn) VALUES ('{contractor_company_name}', '{temp_ssn}')"
        company_result = self.execute_update(contractor_query)
        print(f"Add contractor company: {contractor_company_name} for employee {temp_ssn}")

        return company_result

    def add_contractor_company_to_employee(self, temp_ssn, contractor_company_name):
        ensure_not_empty(temp_ssn)
        ensure_not_empty(contractor_company_name)

        employee_result = self.execute_query(
            f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'"
        )

        if len(employee_result) == 0:
            return {"success": False, "error": "Temporary employee does not exist"}

        company_result = self.execute_query(
            f"SELECT * FROM Contractor_Company WHERE Temp_Employee_Ssn = '{temp_ssn}'"
        )

        if len(company_result) > 0:
            return {"success": False, "error": "Contractor company already exists for this employee"}

        query = f"INSERT INTO Contractor_Company (name, Temp_Employee_Ssn) VALUES ('{contractor_company_name}', '{temp_ssn}')"
        print(f"Added contractor company: {contractor_company_name} for employee {temp_ssn}")
        return self.execute_update(query)

    def get_temp_employee_with_company(self, temp_ssn):
        ensure_not_empty(temp_ssn)

        query = f"""
            SELECT te.TempSsn, te.Company_name, cc.name as Contractor_Company_Name
            FROM Temporary_Employee te
            LEFT JOIN Contractor_Company cc ON te.TempSsn = cc.Temp_Employee_Ssn
            WHERE te.TempSsn = '{temp_ssn}'
        """

        result = self.execute_query(query)

        if len(result) == 0:
            print(f"Temporary employee {temp_ssn} does not exist.")
            return result

        print(f"Get employee: {result[0]['TempSsn']}, company: {result[0]['Company_name']}")
        if result[0]['Contractor_Company_Name']:
            print(f"Contractor company: {result[0]['Contractor_Company_Name']}")

        return result

    def get_temp_employee_by_ssn(self, temp_ssn):
        ensure_not_empty(temp_ssn)
        query = f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'"
        result = self.execute_query(query)
        if len(result) != 0:
            print("Get ", result[0]['TempSsn'], " ", result[0]['Company_name'])
        else:
            print("There is not such temporary employee exist")
        return result

    def get_all_temp_employees(self):
        query = "SELECT * FROM Temporary_Employee ORDER BY Company_name, TempSsn"
        result = self.execute_query(query)
        if len(result) != 0:
            for row in result:
                print(f"TempSsn: {row['TempSsn']}, Company_name: {row['Company_name']}")
        else:
            print("There is not temporary employee now")
        return result

    def get_all_temp_employees_with_companies(self):
        query = """
            SELECT te.TempSsn, te.Company_name, cc.name as Contractor_Company_Name
            FROM Temporary_Employee te
            LEFT JOIN Contractor_Company cc ON te.TempSsn = cc.Temp_Employee_Ssn
            ORDER BY te.Company_name, te.TempSsn
        """

        result = self.execute_query(query)

        if len(result) != 0:
            for row in result:
                print(f"TempSsn: {row['TempSsn']}, Company_name: {row['Company_name']}")
                if row['Contractor_Company_Name']:
                    print(f"  Contractor: {row['Contractor_Company_Name']}")
        else:
            print("There are no temporary employees")

        return result

    def delete_temp_employee(self, temp_ssn):
        ensure_not_empty(temp_ssn)

        check_query = f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'"
        result = self.execute_query(check_query)

        if len(result) == 0:
            print(f"Temporary employee {temp_ssn} does not exist.")
            return {"success": False, "error": "Temporary employee not found"}

        delete_temp_supervise_query = f"DELETE FROM TempSupervise WHERE Supervisee_Ssn_temp_employee = '{temp_ssn}'"
        self.execute_update(delete_temp_supervise_query)

        delete_contractor_query = f"DELETE FROM Contractor_Company WHERE Temp_Employee_Ssn = '{temp_ssn}'"
        self.execute_update(delete_contractor_query)

        delete_assignments_query = f"DELETE FROM Temp_Employee_Work_On WHERE Temp_Working_Worker_Ssn = '{temp_ssn}'"
        self.execute_update(delete_assignments_query)

        delete_employee_query = f"DELETE FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'"
        print(f"Deleted temporary employee: (ssn) {temp_ssn}")
        return self.execute_update(delete_employee_query)

    def update_contractor_company(self, temp_employee_ssn, new_company_name):
        ensure_not_empty(temp_employee_ssn)
        ensure_not_empty(new_company_name)

        company_query = f"SELECT * FROM Contractor_Company WHERE Temp_Employee_Ssn = '{temp_employee_ssn}'"
        company_result = self.execute_query(company_query)

        if len(company_result) == 0:
            return {"success": False, "error": "Contractor company not found"}

        query = f"UPDATE Contractor_Company SET name = '{new_company_name}' WHERE Temp_Employee_Ssn = '{temp_employee_ssn}'"
        print(f"Updated contractor company for employee {temp_employee_ssn} to {new_company_name}")
        return self.execute_update(query)
