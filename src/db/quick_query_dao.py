from .base_dao import BaseDAO
from .validators import Validators


class QuickQueryDAO(BaseDAO):

    # ------ these are all the functions related to the "activity" entity set ------

    # 1. get the basic information of an activity by the primary key
    def get_activity(self, activity_time, activity_building, activity_floor, activity_room_num):
        query = f"SELECT * FROM Activity WHERE Activity_Time = '{activity_time}' AND Activity_Building = '{activity_building}' AND Activity_Floor = '{activity_floor}' AND Activity_RoomNum = '{activity_room_num}'"
        result = self.execute_query(query)
        print(f"activity type: {result[0]['Activity_Type']}, chemical required: {result[0]['Require_Chemical']}")
        return result
    # finished

    # 2. create a new activity
    def create_activity(self, activity_time, activity_type, require_chemical, activity_building, activity_floor, activity_room_num):
        if Validators.validate_date(activity_time) and Validators.validate_activity_type(activity_type) and Validators.validate_chemical_requirement(require_chemical) and Validators.validate_floor(activity_floor) and Validators.validate_room(activity_room_num):
            query = f"SELECT * FROM Activity WHERE Activity_Time = '{activity_time}' AND Activity_Building = '{activity_building}' AND Activity_Floor = '{activity_floor}' AND Activity_RoomNum = '{activity_room_num}'"
            result = self.execute_query(query)
            if len(result) == 0:
                query = f"INSERT INTO Activity (Activity_Time, Activity_Type, Require_Chemical, Activity_Building, Activity_Floor, Activity_RoomNum) VALUES ('{activity_time}', '{activity_type}', '{require_chemical}', '{activity_building}', '{activity_floor}', '{activity_room_num}')"
                return self.execute_update(query)
        else:
            print("Input not qualified! Check the user manual!")
    # finished

    # 3. get all current activities
    def get_all_activities(self):
        query = "SELECT * FROM Activity ORDER BY Activity_Time DESC, Activity_Building, Activity_Floor"
        result = self.execute_query(query)
        for row in result:
            print(
                f"Activity_time: {row['Activity_Time']}, Activity_type: {row['Activity_Type']}, Require_chemical: {row['Require_chemical']}, Activity_building: {row['Activity_building']}, Activity_floor: {row['Activity_floor']}, Activity_room_num: {row['Activity_room_num']}"
            )
        return result
    # finished

    # 4. assign a manager to manage an activity
    def assign_manager_to_activity(self, manager_ssn, activity_time, activity_building, activity_floor,
                                   activity_room_num):
        if Validators.validate_date(activity_time):
            query = f"SELECT * FROM Mid_Level_Manage_Activity WHERE Manage_Activity_Building = {activity_building} AND Manage_Activity_Floor = {activity_floor} AND Manage_Activity_RoomNum = {activity_room_num} AND Manage_Activity_Time = {activity_time}"
            result = self.execute_query(query)
            if len(result) == 0:
                query = f"INSERT INTO Mid_Level_Manage_Activity (Manager_Ssn, Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time) VALUES ('{manager_ssn}', '{activity_building}', '{activity_floor}', '{activity_room_num}', '{activity_time}')"
                return self.execute_update(query)
        else:
            print("Input date not validated!")
    # finished

    # 5. assign a work to an employee
    def assign_employee_to_activity(self, working_time, working_building, working_floor, working_room_number,
                                    working_worker_ssn):
        if Validators.validate_date(working_time):
            query = f"SELECT * FROM Employee_Work_On WHERE Working_Building = {working_building} AND Working_Floor = {working_floor} AND Working_Room_number = {working_room_number} AND Working_Time = {working_time}"
            result = self.execute_query(query)
            if len(result) == 0:
                query = f"INSERT INTO Employee_Work_On (Working_Time, Working_Building, Working_Floor, Working_Room_number, Working_Worker_Ssn) VALUES ('{working_time}', '{working_building}', '{working_floor}', '{working_room_number}', '{working_worker_ssn}')"
                return self.execute_update(query)
        else:
            print("Input date not validated!")
    # finished

    # 6. assign a work to a temp-employee
    def assign_temp_employee_to_activity(self, temp_working_time, temp_working_building, temp_working_floor,
                                         temp_working_room_number, temp_working_worker_ssn):
        if Validators.validate_date(temp_working_time):
            query = f"SELECT * FROM Temp_Employee_Work_On WHERE Temp_Working_Building = {temp_working_building} AND Temp_Working_Floor = {temp_working_floor} AND Temp_Working_Room_number = {temp_working_room_number} AND Temp_Working_Time = {temp_working_time} AND Temp_Working_Worker_Ssn = {temp_working_worker_ssn}"
            result = self.execute_query(query)
            if result == 0:
                query = f"INSERT INTO Temp_Employee_Work_On (Temp_Working_Time, Temp_Working_Building, Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn) VALUES ('{temp_working_time}', '{temp_working_building}', '{temp_working_floor}', '{temp_working_room_number}', '{temp_working_worker_ssn}')"
                return self.execute_update(query)
        else:
            print("Input date not qualified!")
    # finished

    # 7. apply an activity to a location
    def create_applied_to(self, applied_time, applied_building, applied_floor, applied_room_number, applied_reason):
        query = f"INSERT INTO Applied_To (Applied_Time, Applied_Building, Applied_Floor, Applied_Room_number, Applied_Reason) VALUES ('{applied_time}', '{applied_building}', '{applied_floor}', '{applied_room_number}', '{applied_reason}')"
        return self.execute_update(query)
    # finished

    def remove_manager_from_activity(self, manager_ssn, activity_time, activity_building, activity_floor,
                                     activity_room_num):
        query = f"SELECT * FROM Mid_Level_Manage_Activity WHERE Manage_Activity_Building = {activity_building} AND Manage_Activity_Floor = {activity_floor} AND Manage_Activity_RoomNum = {activity_room_num} AND Manage_Activity_Time = {activity_time}"
        result = self.execute_query(query)
        if len(result) != 0:
            query = f"DELETE FROM Mid_Level_Manage_Activity WHERE Manager_Ssn = '{manager_ssn}' AND Manage_Activity_Building = '{activity_building}' AND Manage_Activity_Floor = '{activity_floor}' AND Manage_Activity_RoomNum = '{activity_room_num}' AND Manage_Activity_Time = '{activity_time}'"
            return self.execute_update(query)
        else:
            print("Not exists!")

    def remove_employee_from_activity(self, working_time, working_building, working_floor, working_room_number,
                                      working_worker_ssn):
        query = f"SELECT * FROM Employee_Work_On WHERE Working_Building = {working_building} AND Working_Floor = {working_floor} AND Working_Room_number = {working_room_number} AND Working_Time = {working_time}"
        result = self.execute_query(query)
        if len(result) != 0:
            query = f"DELETE FROM Employee_Work_On WHERE Working_Time = '{working_time}' AND Working_Building = '{working_building}' AND Working_Floor = '{working_floor}' AND Working_Room_number = '{working_room_number}' AND Working_Worker_Ssn = '{working_worker_ssn}'"
            return self.execute_update(query)
        else:
            print("Not exists!")

    def remove_temp_employee_from_activity(self, temp_working_time, temp_working_building, temp_working_floor,
                                           temp_working_room_number, temp_working_worker_ssn):
        query = f"SELECT * FROM Temp_Employee_Work_On WHERE Temp_Working_Building = {temp_working_building} AND Temp_Working_Floor = {temp_working_floor} AND Temp_Working_Room_number = {temp_working_room_number} AND Temp_Working_Time = {temp_working_time} AND Temp_Working_Worker_Ssn = {temp_working_worker_ssn}"
        result = self.execute_query(query)
        if len(result) != 0:
            query = f"DELETE FROM Temp_Employee_Work_On WHERE Temp_Working_Time = '{temp_working_time}' AND Temp_Working_Building = '{temp_working_building}' AND Temp_Working_Floor = '{temp_working_floor}' AND Temp_Working_Room_number = '{temp_working_room_number}' AND Temp_Working_Worker_Ssn = '{temp_working_worker_ssn}'"
            return self.execute_update(query)
        else:
            print("Not exists!")



    # get all current standard employees in the database
    def get_all_employees(self):
        result = self.execute_query("SELECT * FROM Employee")
        for row in result:
            print(f"Ssn: {row['Ssn']}, Name: {row['Name']}, Level: {row['Emp_Level']}")
        return result

    # get an employee's name by its ssn
    def get_employee_by_ssn(self, ssn):
        result = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{ssn}'",
        )
        if len(result) > 0:
            print(result[0]['Name'])
            return result[0]['Name']
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
            return result
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

    # delete an employee
    def delete_employee(self, ssn):
        result = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{ssn}'",
        )
        if len(result) > 0:
            query = f"DELETE FROM Employee WHERE Ssn = '{ssn}'"
            return self.execute_update(query)
        else:
            print("Employee not exists. Insert first.")

    # insert a new campus location to the database
    def create_location(self, building, floor, room_number):
       result = self.execute_query(
            f"SELECT * FROM Location WHERE Building = '{building}' AND Floor = '{floor}' AND RoomNumber = '{room_number}'",
       )
       if len(result) == 0:
           return self.execute_update(
               f"INSERT INTO Location (Building, Floor, Room_number) VALUES ('{building}', '{floor}', '{room_number}')"
           )
       else:
           print("This location exists!")

    def check_location(self, building, floor, room_number):
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if floor_valid and room_valid:
            result = self.execute_query(
                f"SELECT * FROM Location WHERE Building = '{building}' AND Floor = '{floor}' AND RoomNumber = '{room_number}'"
            )
            if len(result) == 0:
                attention = "It exists!"
                print(attention)
                return attention
            else:
                attention = "Not exists!"
                print(attention)
                return attention





    def get_all_locations(self):

        result = self.execute_query("SELECT * FROM Location")
        for row in result:
            print(f"Building: {row['Building']}, Floor: {row['Floor']}, Room_number: {row['Room_number']}")
        return result

    def get_locations_by_building(self, building):
        result = self.execute_query(
            f"SELECT * FROM Location WHERE Building = '{building}'",
        )
        for row in result:
            print(f"Building: {row['Building']}, Floor: {row['Floor']}, Room_number: {row['Room_number']}")
        return result

    def get_vacant_offices(self):
        result = self.execute_query(
            f"SELECT * FROM Office WHERE OwnerSsn IS NULL"
        )
        for row in result:
            print(
                f"Building: {row['Office_Building']}, Floor: {row['Office_Floor']}, Room_number: {row['Office_RoomNum']}"
            )
        return result

    def assign_office_to_employee(self, building, floor, room_number, owner_ssn):
        result = self.execute_query(
            f"SELECT * FROM Office WHERE OwnerSsn = '{owner_ssn}"
        )
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if floor_valid and room_valid:
            if len(result) == 0:
                self.execute_query(
                    f"UPDATE Office SET OwnerSsn = '{owner_ssn}' WHERE Office_Building = '{building}' AND Office_Floor = '{floor}' AND Office_RoomNum = '{room_number}'"
                )
            else:
                message = "The employee has an office."
                print(message)
                return message
        else:
            print("Not valid!")
            return "Not valid!"

    def vacate_office(self, building, floor, room_number):

        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if floor_valid and room_valid:
            self.execute_query(
                f"UPDATE Office SET OwnerSsn = NULL WHERE Office_Building = '{building}' AND Office_Floor = '{floor}' AND Office_RoomNum = '{room_number}'"
            )

        else:
            print("Not valid.")
            return "Not valid."

    def get_mid_level_managers(self):
        result = self.execute_query(
            f"SELECT Name FROM Employee WHERE Emp_Level = mid_level manager",
        )
        for row in result:
            print(f"Mid_level manager Mr./Ms. {row['Name']}")
        return result

    def get_activities_by_date_range(self, start_date, end_date):
        result = self.execute_query(
            f"SELECT * FROM Activity WHERE Activity_Time BETWEEN '{start_date}' AND '{end_date}'",
        )
        for row in result:
            print(f"Activity_Time: {row['Activity_Time']}, Activity_Type: {row['Activity_Type']}, Require_Chemical: {row['Require_Chemical']},Activity_Type: {row['Activity_Type']}, Require_Chemical: {row['Require_Chemical']}")
        return result

    def get_manager_activity_counts(self,manager_ssn):
        result = self.execute_query(
            f"SELECT * FROM Mid_Level_Manage_Activity  WHERE Manager_Ssn = '{manager_ssn}'",
        )
        count = len(result)
        print(f"The number of activities managed by manager {manager_ssn} is {count}.")
        return count

    def get_employees_in_certain_building(self, activity_date, building):
        result = self.execute_query(
            f"SELECT Working_Worker_Ssn FROM Employee_Work_On WHERE Working_Building = '{building}' AND Activity_Time = '{activity_date}'",
        )
        print("the workers' Ssns are:")
        for row in result:
            print(f"{row['Working_Worker_Ssn']}")
        return result



    def get_contractor_employee_counts(self):
        result = self.execute_query(
            f"SELECT * FROM Temporary_Employee",
        )
        i = len(result)
        print(f"the contract worker count is: {i}")
        return i





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








    def create_temp_employee_with_company(self, temp_ssn, company_name, contractor_company_name):


        result = self.execute_query(
            f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'",
        )

        if len(result) > 0:
            print(f"Temporary employee {temp_ssn} already exists.")
            return "Already exists!"

        query = f"INSERT INTO Temporary_Employee (TempSsn, Company_name) VALUES ('{temp_ssn}', '{company_name}')"
        contractor_query = f"INSERT INTO Contractor_Company (name, Temp_Employee_Ssn) VALUES ('{contractor_company_name}', '{temp_ssn}')"

        print("Add new temporary employee: (ssn)", temp_ssn)
        print(f"Add contractor company: {contractor_company_name} for employee {temp_ssn}")
        return self.execute_update(query) and self.execute_update(contractor_query)



    def get_temp_employee_with_company(self, temp_ssn):


        query = f"""
            SELECT te.TempSsn, te.Company_name, cc.name as Contractor_Company_Name
            FROM Temporary_Employee te
            LEFT JOIN Contractor_Company cc ON te.TempSsn = cc.Temp_Employee_Ssn
            WHERE te.TempSsn = '{temp_ssn}'
        """

        result = self.execute_query(query)

        if len(result) == 0:
            print(f"Temporary employee {temp_ssn} does not exist.")
            return "not exist"

        print(f"Get employee: {result[0]['TempSsn']}, company: {result[0]['Company_name']}")
        if result[0]['Contractor_Company_Name']:
            print(f"Contractor company: {result[0]['Contractor_Company_Name']}")

        return result

    def get_temp_employee_by_ssn(self, temp_ssn):

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


        check_query = f"SELECT * FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'"
        result = self.execute_query(check_query)

        if len(result) == 0:
            print(f"Temporary employee {temp_ssn} does not exist.")
            return {"success": False, "error": "Temporary employee not found"}



        delete_employee_query = f"DELETE FROM Temporary_Employee WHERE TempSsn = '{temp_ssn}'"
        print(f"Deleted temporary employee: (ssn) {temp_ssn}")
        return self.execute_update(delete_employee_query)

    def update_contractor_company(self, temp_employee_ssn, new_company_name):


        company_query = f"SELECT * FROM Contractor_Company WHERE Temp_Employee_Ssn = '{temp_employee_ssn}'"
        company_result = self.execute_query(company_query)

        if len(company_result) == 0:
            return {"success": False, "error": "Contractor company not found"}

        query = f"UPDATE Contractor_Company SET name = '{new_company_name}' WHERE Temp_Employee_Ssn = '{temp_employee_ssn}'"
        print(f"Updated contractor company for employee {temp_employee_ssn} to {new_company_name}")
        return self.execute_update(query)

    def execute_custom_sql(self, sql_query):
        """
        执行自定义SQL查询，支持SELECT、INSERT、UPDATE、DELETE等操作
        """
        # 检查SQL语句是否为空
        if not sql_query or not sql_query.strip():
            print("SQL query cannot be empty.")
            return "Empty query"

        # 直接使用原始查询，不进行任何引号处理
        clean_sql = sql_query.strip()
        sql_lower = clean_sql.lower()

        # 安全检查
        dangerous_operations = ['drop', 'truncate', 'alter table', 'create table']
        if any(op in sql_lower for op in dangerous_operations):
            print("⚠️  WARNING: Potentially destructive SQL operation detected!")
            print(f"Query: {clean_sql}")
            confirm = input("Type 'CONFIRM' to proceed, anything else to cancel: ")
            if confirm != 'CONFIRM':
                print("Query execution cancelled.")
                return "Execution cancelled by user"

        # 根据SQL类型执行不同的操作
        if (sql_lower.startswith('select') or
                sql_lower.startswith('show') or
                sql_lower.startswith('describe') or
                sql_lower.startswith('with')):
            # 执行查询语句
            print(f"🔍 Executing query: {clean_sql}")
            result = self.execute_query(clean_sql)

            if len(result) == 0:
                print("✅ Query executed successfully. No results returned.")
                return []
            else:
                print(f"✅ Query executed successfully. Returned {len(result)} row(s).")

                # 美化输出
                if result:
                    headers = list(result[0].keys())

                    # 计算每列的最大宽度
                    col_widths = []
                    for header in headers:
                        max_width = len(str(header))
                        for row in result:
                            max_width = max(max_width, len(str(row.get(header, ''))))
                        col_widths.append(max_width)

                    # 打印表头
                    header_line = " | ".join(str(header).ljust(col_widths[i]) for i, header in enumerate(headers))
                    separator = "-+-".join('-' * width for width in col_widths)

                    print(header_line)
                    print(separator)

                    # 打印数据行
                    for row in result:
                        row_line = " | ".join(
                            str(row.get(header, '')).ljust(col_widths[i]) for i, header in enumerate(headers))
                        print(row_line)

                return result

        else:
            # 执行更新语句（INSERT, UPDATE, DELETE等）
            print(f"⚡ Executing update: {clean_sql}")
            affected_rows = self.execute_update(clean_sql)

            if affected_rows:
                print(f"✅ Update executed successfully. {affected_rows} row(s) affected.")
                return affected_rows
            else:
                print("✅ Update executed successfully.")
                return 0
