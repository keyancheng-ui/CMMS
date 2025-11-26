from .connection import DatabaseConnection
from .validators import Validators, ensure_not_empty

class ActivityDAO:
    def __init__(self):
        pass

    def create_activity(self, activity_time, activity_type, require_chemical, activity_building, activity_floor, activity_room_num):
        try:
            ensure_not_empty(activity_time)
            ensure_not_empty(activity_type)
            ensure_not_empty(activity_building)

            valid, msg = Validators.validate_date(activity_time)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_activity_type(activity_type)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_chemical_requirement(require_chemical)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_building(activity_building)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_floor(activity_floor)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_room(activity_room_num)
            if not valid:
                return {"success": False, "error": msg}

            db = DatabaseConnection()
            query = """
                INSERT INTO Activity (Activity_Time, Activity_Type, Require_Chemical, 
                                    Activity_Building, Activity_Floor, Activity_RoomNum)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor = db.connection.cursor()
            cursor.execute(query, (activity_time, activity_type, require_chemical, 
                                 activity_building, activity_floor, activity_room_num))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {
                "Activity_Time": activity_time,
                "Activity_Type": activity_type,
                "Require_Chemical": require_chemical,
                "Activity_Building": activity_building,
                "Activity_Floor": activity_floor,
                "Activity_RoomNum": activity_room_num
            }}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_activity(self, activity_time, activity_building, activity_floor, activity_room_num):
        try:
            ensure_not_empty(activity_time)
            ensure_not_empty(activity_building)

            db = DatabaseConnection()
            query = """
                SELECT * FROM Activity 
                WHERE Activity_Time = %s AND Activity_Building = %s 
                AND Activity_Floor = %s AND Activity_RoomNum = %s
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (activity_time, activity_building, activity_floor, activity_room_num))
            result = cursor.fetchone()
            cursor.close()
            db.close()
            
            if result:
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": "Activity not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_activities(self):
        try:
            db = DatabaseConnection()
            query = "SELECT * FROM Activity ORDER BY Activity_Time DESC, Activity_Building, Activity_Floor"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def assign_manager_to_activity(self, manager_ssn, activity_time, activity_building, activity_floor, activity_room_num):
        try:
            ensure_not_empty(manager_ssn)
            ensure_not_empty(activity_time)
            ensure_not_empty(activity_building)

            db = DatabaseConnection()
            query = """
                INSERT INTO Mid_Level_Manage_Activity (Manager_Ssn, Manage_Activity_Building, 
                                                     Manage_Activity_Floor, Manage_Activity_RoomNum, Manage_Activity_Time)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor = db.connection.cursor()
            cursor.execute(query, (manager_ssn, activity_building, activity_floor, activity_room_num, activity_time))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {
                "Manager_Ssn": manager_ssn,
                "Manage_Activity_Building": activity_building,
                "Manage_Activity_Floor": activity_floor,
                "Manage_Activity_RoomNum": activity_room_num,
                "Manage_Activity_Time": activity_time
            }}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def assign_employee_to_activity(self, working_time, working_building, working_floor, working_room_number, working_worker_ssn):
        try:
            ensure_not_empty(working_time)
            ensure_not_empty(working_building)
            ensure_not_empty(working_worker_ssn)

            db = DatabaseConnection()
            query = """
                INSERT INTO Employee_Work_On (Working_Time, Working_Building, Working_Floor, 
                                            Working_Room_number, Working_Worker_Ssn)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor = db.connection.cursor()
            cursor.execute(query, (working_time, working_building, working_floor, working_room_number, working_worker_ssn))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {
                "Working_Time": working_time,
                "Working_Building": working_building,
                "Working_Floor": working_floor,
                "Working_Room_number": working_room_number,
                "Working_Worker_Ssn": working_worker_ssn
            }}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def assign_temp_employee_to_activity(self, temp_working_time, temp_working_building, temp_working_floor, temp_working_room_number, temp_working_worker_ssn):
        try:
            ensure_not_empty(temp_working_time)
            ensure_not_empty(temp_working_building)
            ensure_not_empty(temp_working_worker_ssn)

            db = DatabaseConnection()
            query = """
                INSERT INTO Temp_Employee_Work_On (Temp_Working_Time, Temp_Working_Building, 
                                                 Temp_Working_Floor, Temp_Working_Room_number, Temp_Working_Worker_Ssn)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor = db.connection.cursor()
            cursor.execute(query, (temp_working_time, temp_working_building, temp_working_floor, 
                                 temp_working_room_number, temp_working_worker_ssn))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {
                "Temp_Working_Time": temp_working_time,
                "Temp_Working_Building": temp_working_building,
                "Temp_Working_Floor": temp_working_floor,
                "Temp_Working_Room_number": temp_working_room_number,
                "Temp_Working_Worker_Ssn": temp_working_worker_ssn
            }}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_applied_to(self, applied_time, applied_building, applied_floor, applied_room_number, applied_reason):
        try:
            ensure_not_empty(applied_time)
            ensure_not_empty(applied_building)
            ensure_not_empty(applied_reason)

            valid, msg = Validators.validate_date(applied_time)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_building(applied_building)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_floor(applied_floor)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_room(applied_room_number)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_applied_reason(applied_reason)
            if not valid:
                return {"success": False, "error": msg}

            db = DatabaseConnection()
            query = """
                INSERT INTO Applied_To (Applied_Time, Applied_Building, Applied_Floor, 
                                      Applied_Room_number, Applied_Reason)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor = db.connection.cursor()
            cursor.execute(query, (applied_time, applied_building, applied_floor, applied_room_number, applied_reason))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {
                "Applied_Time": applied_time,
                "Applied_Building": applied_building,
                "Applied_Floor": applied_floor,
                "Applied_Room_number": applied_room_number,
                "Applied_Reason": applied_reason
            }}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
