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