from .base_dao import BaseDAO
from .validators import Validators


class TempEmployeeDAO(BaseDAO):

    def get_all_temp_employee(self):
        result = self.execute_query("SELECT * FROM Temporary_Employee")
        for row in result:
            print(f"Ssn: {row[0]}, Company: {row[1]}")

    def create_temp_employee(self, temp_ssn, company_name):
        result = self.execute_query("SELECT TempSsn FROM Temporary_Employee")
        ssn_list = []
        for row in result:
            ssn_list.append(row[0])
        if temp_ssn not in ssn_list:
            if Validators.validate_company_name(company_name):
                return self.execute_update(
                    f"INSERT INTO Temporary_Employee (TempSsn, Company_name) VALUES ('{temp_ssn}', '{company_name}')"
                )
            else:
                Validators.validate_company_name(company_name)
        else:
            print("This employee already exists.")

    def get_temp_employee_by_ssn(self, temp_ssn):
        result = self.execute_query("SELECT TempSsn FROM Temporary_Employee")
        ssn_list = []
        for row in result:
            ssn_list.append(row[0])
        if temp_ssn in ssn_list:
            temp_list = self.execute_query(f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'")
            for row in temp_list:
                print(f"TempSsn: {row[0]}, Company: {row[1]}")
        else:
            print("Employee not exist.")
            return None

    def get_employee_for_a_company(self, company_name):
        result = self.execute_query("SELECT Company_name FROM Temporary_Employee")
        company_list = []
        for row in result:
            company_list.append(row[0])
        if company_name in company_list:
            ssn_list = self.execute_query(f"SELECT TempSsn FROM Temporary_Employee WHERE Company_name = '{company_name}'")
            for row in ssn_list:
                print(row[0])
        else:
            print("Company not exists.")
