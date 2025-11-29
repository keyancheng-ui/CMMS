from .connection import DatabaseConnection
from .base_dao import BaseDAO
from .validators import Validators, ensure_not_empty


class ActivityDAO(BaseDAO):

    def get_activity(self, activity_time, activity_building, activity_floor, activity_room_num):
        try:
            query = f"SELECT * FROM Activity WHERE Activity_Time = '{activity_time}' AND Activity_Building = '{activity_building}' AND Activity_Floor = '{activity_floor}' AND Activity_RoomNum = '{activity_room_num}'"
            result = self.execute_query(query)
            return result

        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_activity(self, activity_time, activity_type, require_chemical, activity_building, activity_floor, activity_room_num):
        try:
            ensure_not_empty(activity_time)
            ensure_not_empty(activity_type)
            ensure_not_empty(activity_building)

            if Validators.validate_date(activity_time) and Validators.validate_activity_type(activity_type) and Validators.validate_chemical_requirement(require_chemical) and Validators.validate_building(activity_building) and Validators.validate_floor(activity_floor) and Validators.validate_room(activity_room_num):
                if self.get_activity(activity_time, activity_building, activity_floor, activity_room_num).len() != 0:
                    query = f"INSERT INTO Activity (Activity_Time, Activity_Type, Require_Chemical, Activity_Building, Activity_Floor, Activity_RoomNum) VALUES ('{activity_time}', '{activity_type}', '{require_chemical}', '{activity_building}', '{activity_floor}', '{activity_room_num}')"
                    return self.execute_update(query)

            else:
                return Validators.validate_date(activity_time) and Validators.validate_activity_type(activity_type) and Validators.validate_chemical_requirement(require_chemical) and Validators.validate_building(activity_building) and Validators.validate_floor(activity_floor) and Validators.validate_room(activity_room_num)

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_activities(self):
        try:
            query = "SELECT * FROM Activity ORDER BY Activity_Time DESC, Activity_Building, Activity_Floor"
            result = self.execute_query(query)

            for tuple in result:
                print(
                    f"Activity_time: {tuple[0]}, Activity_type: {tuple[1]}, Require_chemical: {tuple[2]}, Activity_building: {tuple[3]}, Activity_floor: {tuple[4]}, Activity_room_num: {tuple[5]}")

            return result

        except Exception as e:
            return {"success": False, "error": str(e)}

    def assign_manager_to_activity(self, manager_ssn, activity_time, activity_building, activity_floor,
                                   activity_room_num):
        try:
            ensure_not_empty(manager_ssn)
            ensure_not_empty(activity_time)
            ensure_not_empty(activity_building)

            query = f"INSERT INTO Mid_Level_Manage_Activity (Manager_Ssn, Manage_Activity_Building, Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time) VALUES ('{manager_ssn}', '{activity_building}', '{activity_floor}', '{activity_room_num}', '{activity_time}')"

            result = self.execute_update(query)

            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def assign_employee_to_activity(self, working_time, working_building, working_floor, working_room_number,
                                    working_worker_ssn):
        try:
            ensure_not_empty(working_time)
            ensure_not_empty(working_building)
            ensure_not_empty(working_worker_ssn)

            query = f"INSERT INTO Employee_Work_On (Working_Time, Working_Building, Working_Floor, Working_Room_number, Working_Worker_Ssn) VALUES ('{working_time}', '{working_building}', '{working_floor}', '{working_room_number}', '{working_worker_ssn}')"

            result = self.execute_update(query)

            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def assign_temp_employee_to_activity(self, temp_working_time, temp_working_building, temp_working_floor,
                                         temp_working_room_number, temp_working_worker_ssn):
        try:
            ensure_not_empty(temp_working_time)
            ensure_not_empty(temp_working_building)
            ensure_not_empty(temp_working_worker_ssn)

            query = f"INSERT INTO Temp_Employee_Work_On (Temp_Working_Time, Temp_Working_Building, Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn) VALUES ('{temp_working_time}', '{temp_working_building}', '{temp_working_floor}', '{temp_working_room_number}', '{temp_working_worker_ssn}')"

            result = self.execute_update(query)

            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_applied_to(self, applied_time, applied_building, applied_floor, applied_room_number, applied_reason):
        try:
            ensure_not_empty(applied_time)
            ensure_not_empty(applied_building)
            ensure_not_empty(applied_reason)

            if not (Validators.validate_date(applied_time) and
                    Validators.validate_building(applied_building) and
                    Validators.validate_floor(applied_floor) and
                    Validators.validate_room(applied_room_number) and
                    Validators.validate_applied_reason(applied_reason)):
                return {"success": False, "error": "Invalid input data"}

            query = f"INSERT INTO Applied_To (Applied_Time, Applied_Building, Applied_Floor, Applied_Room_number, Applied_Reason) VALUES ('{applied_time}', '{applied_building}', '{applied_floor}', '{applied_room_number}', '{applied_reason}')"


            result = self.execute_update(query)

            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def remove_manager_from_activity(self, manager_ssn, activity_time, activity_building, activity_floor,
                                     activity_room_num):
        try:
            ensure_not_empty(manager_ssn)
            ensure_not_empty(activity_time)
            ensure_not_empty(activity_building)

            query = f"DELETE FROM Mid_Level_Manage_Activity WHERE Manager_Ssn = '{manager_ssn}' AND Manage_Activity_Building = '{activity_building}' AND Manage_Activity_Floor = '{activity_floor}' AND Manage_Activity_RoomNum = '{activity_room_num}' AND Manage_Activity_Time = '{activity_time}'"

            result = self.execute_update(query)

            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def remove_employee_from_activity(self, working_time, working_building, working_floor, working_room_number,
                                      working_worker_ssn):
        try:
            ensure_not_empty(working_time)
            ensure_not_empty(working_building)
            ensure_not_empty(working_worker_ssn)

            query = f"DELETE FROM Employee_Work_On WHERE Working_Time = '{working_time}' AND Working_Building = '{working_building}' AND Working_Floor = '{working_floor}' AND Working_Room_number = '{working_room_number}' AND Working_Worker_Ssn = '{working_worker_ssn}'"

            result = self.execute_update(query)

            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def remove_temp_employee_from_activity(self, temp_working_time, temp_working_building, temp_working_floor,
                                           temp_working_room_number, temp_working_worker_ssn):
        try:
            ensure_not_empty(temp_working_time)
            ensure_not_empty(temp_working_building)
            ensure_not_empty(temp_working_worker_ssn)

            query = f"DELETE FROM Temp_Employee_Work_On WHERE Temp_Working_Time = '{temp_working_time}' AND Temp_Working_Building = '{temp_working_building}' AND Temp_Working_Floor = '{temp_working_floor}' AND Temp_Working_Room_number = '{temp_working_room_number}' AND Temp_Working_Worker_Ssn = '{temp_working_worker_ssn}'"

            result = self.execute_update(query)

            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

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

    # delete an employee
    def delete_employee(self, ssn):
        result = self.execute_query(
            f"SELECT * FROM Employee WHERE Ssn = '{ssn}'",
        )
        if len(result) > 0:
            result = self.execute_query(
                f"SELECT * FROM Employee_Supervision WHERE Supervisor_Ssn = '{ssn}' OR Supervisee_Ssn = '{ssn}'"
            )
            query1 = f"DELETE FROM Employee WHERE Ssn = '{ssn}'"
            if len(result) > 0:
                query2 = f"DELETE FROM Employee_Supervision WHERE Supervisor_Ssn = '{ssn}' OR Supervisee_Ssn = '{ssn}'"
                self.execute_update(query2)
            return self.execute_update(query1)
        else:
            print("Employee not exists. Insert first.")


from .base_dao import BaseDAO
from .validators import Validators


class LocationDAO(BaseDAO):

    # insert a new campus location to the database
    def create_location(self, building, floor, room_number):
        build_valid, build_msg = Validators.validate_building(building)
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if build_valid and floor_valid and room_valid:
            result = self.execute_query(
                f"SELECT * FROM Location WHERE Building = '{building}' AND Floor = '{floor}' AND RoomNumber = '{room_number}'",
            )
            if len(result) == 0:
                return self.execute_update(
                    f"INSERT INTO Location (Building, Floor, Room_number) VALUES ('{building}', '{floor}', '{room_number}')"
                )
            else:
                print("This location already already exist!")



        else:
            print("insertion is invalid, f**k off.")

    def check_location(self, building, floor, room_number):

        build_valid, build_msg = Validators.validate_building(building)
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if build_valid and floor_valid and room_valid:
            result = self.execute_query(
                f"SELECT * FROM Location WHERE Building = '{building}' AND Floor = '{floor}' AND RoomNumber = '{room_number}'",
            )
            if len(result) == 0:
                print("Ain’t no such place")

            else:
                print("You are right. It is on campus")



        else:
            print("Not valid. Please have some common sense.")

    def get_all_locations(self):

        result = self.execute_query("SELECT * FROM Location")
        for row in result:
            print(f"Building: {row['Building']}, Floor: {row['Floor']}, Room_number: {row['Room_number']}")

    def get_locations_by_building(self, building):
        build_valid, build_msg = Validators.validate_building(building)
        if build_valid:
            result = self.execute_query(
                f"SELECT * FROM Location WHERE Building = '{building}'",
            )
            for row in result:
                print(f"Building: {row['Building']}, Floor: {row['Floor']}, Room_number: {row['Room_number']}")
        else:
            print("Not valid. Please have some common sense.")

    def get_vacant_offices(self):
        result = self.execute_query(
            f"SELECT * FROM Office WHERE OwnerSsn IS NULL"
        )
        for row in result:
            print(
                f"Building: {row['Office_Building']}, Floor: {row['Office_Floor']}, Room_number: {row['Office_RoomNum']}")

    def assign_office_to_employee(self, building, floor, room_number, owner_ssn):
        build_valid, build_msg = Validators.validate_building(building)
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if build_valid and floor_valid and room_valid:
            self.execute_query(
                f"UPDATE Office SET OwnerSsn = '{owner_ssn}' WHERE Office_Building = '{building}' AND Office_Floor = '{floor}' AND Office_RoomNum = '{room_number}'"
            )
        else:
            print("Not valid. This place doesn't exist. What are you f**king thinkin of?")

    def vacate_office(self, building, floor, room_number):
        build_valid, build_msg = Validators.validate_building(building)
        floor_valid, floor_msg = Validators.validate_floor(floor)
        room_valid, room_msg = Validators.validate_room(room_number)
        if build_valid and floor_valid and room_valid:
            self.execute_query(
                f"UPDATE Office SET OwnerSsn = NULL WHERE Office_Building = '{building}' AND Office_Floor = '{floor}' AND Office_RoomNum = '{room_number}'"
            )

        else:
            print("Not valid. This place doesn't exist. What are you f**king thinkin of?")

from .base_dao import BaseDAO


class ReportDAO(BaseDAO):

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
        count = len(result)
        print(f"The number of activities managed by manager {manager_ssn} is {count}.")

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

