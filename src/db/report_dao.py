from newVersion.src.db.base_dao import BaseDAO


class ReportDAO(BaseDAO):
    def __init__(self, db_connection=None, password=None):
        super().__init__(db_connection=db_connection, password=password)

    def get_mid_level_managers_with_offices(self):
        result = self.execute_query(
            f"SELECT Name FROM Employee WHERE Emp_Level = mid_level manager",
        )
        for row in result:
            print(f"Mid_level manager Mr./Ms. {row['Name']}")

    def get_activities_by_date_range(self, start_date, end_date):
        result = self.execute_query(
            f"SELECT * FROM Activity WHERE Activity_Time BETWEEN '{start_date}' AND '{end_date}'",
        )
        for row in result:
            print(f"Activity_Time: {row['Activity_Time']}, Activity_Type: {row['Activity_Type']}, Require_Chemical: {row['Require_Chemical']},Activity_Type: {row['Activity_Type']}, Require_Chemical: {row['Require_Chemical']}"),

    def get_manager_activity_counts(self,manager_ssn):
        result = self.execute_query(
            f"SELECT * FROM Mid_Level_Manage_Activity  WHERE Manager_Ssn = '{manager_ssn}'",
        )
        count = 0
        for row in result:
            count += 1
            print("the activity number is,",count)

    def get_employees_in_certain_building(self, activity_date, building):
        result = self.execute_query(
            f"SELECT Working_Worker_Ssn FROM Employee_Work_On WHERE Working_Building = '{building}' AND Activity_Time = '{activity_date}'",
        )
        print("the workers' Ssns are:")
        for row in result:
            print(f"{row['Working_Worker_Ssn']}")



    def get_contractor_employee_counts(self):
        result = self.execute_query(
            f"SELECT * FROM Temporary_Employee",
        )
        print("the contract worker count is")
        i = 0
        for row in result:
            i += 1
        print(i)



