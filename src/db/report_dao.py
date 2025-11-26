from .connection import DatabaseConnection

class ReportDAO:
    def __init__(self):
        pass

    def get_mid_level_managers_with_offices(self):
        try:
            db = DatabaseConnection()
            query = """
                SELECT 
                    e.Ssn AS manager_id,
                    e.Name AS manager_name,
                    o.Office_Building AS building,
                    o.Office_Floor AS floor,
                    o.Office_RoomNum AS room
                FROM Employee e
                LEFT JOIN Office o ON e.Ssn = o.OwnerSsn
                WHERE e.Emp_Level = 'mid_level manager'
                ORDER BY o.Office_Building, o.Office_Floor
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_cleaning_activities_by_date_range(self, start_date, end_date):
        try:
            db = DatabaseConnection()
            query = """
                SELECT 
                    Activity_Time AS activity_date,
                    Activity_Building AS building,
                    Activity_Floor AS floor,
                    Activity_RoomNum AS room,
                    Require_Chemical AS requires_chemical
                FROM Activity
                WHERE 
                    Activity_Type = 'daily campus cleaning'
                    AND Activity_Time BETWEEN %s AND %s
                ORDER BY Activity_Time, Activity_Building
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (start_date, end_date))
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_manager_activity_counts(self):
        try:
            db = DatabaseConnection()
            query = """
                SELECT 
                    e.Name AS manager_name,
                    e.Ssn AS manager_id,
                    COUNT(m.Manage_Activity_Time) AS activity_count
                FROM Mid_Level_Manage_Activity m
                JOIN Employee e ON m.Manager_Ssn = e.Ssn
                GROUP BY e.Ssn, e.Name
                ORDER BY activity_count DESC
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_employees_in_tech_building_activity(self, activity_date):
        try:
            db = DatabaseConnection()
            query = """
                SELECT 
                    e.Ssn AS employee_id,
                    e.Name AS employee_name,
                    w.Working_Building AS building,
                    w.Working_Floor AS floor,
                    w.Working_Room_number AS room
                FROM Employee_Work_On w
                JOIN Employee e ON w.Working_Worker_Ssn = e.Ssn
                WHERE 
                    w.Working_Building = 'Tech_Building'
                    AND w.Working_Time = %s
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (activity_date,))
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_chemical_activities_with_applications(self):
        try:
            db = DatabaseConnection()
            query = """
                SELECT 
                    a.Activity_Time AS activity_date,
                    a.Activity_Building AS building,
                    a.Activity_Floor AS floor,
                    a.Activity_RoomNum AS room,
                    a.Activity_Type AS activity_type,
                    t.Applied_Reason AS applied_reason
                FROM Activity a
                JOIN Applied_To t ON 
                    a.Activity_Time = t.Applied_Time 
                    AND a.Activity_Building = t.Applied_Building 
                    AND a.Activity_Floor = t.Applied_Floor 
                    AND a.Activity_RoomNum = t.Applied_Room_number
                WHERE a.Require_Chemical = 1
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_contractor_employee_counts(self):
        try:
            db = DatabaseConnection()
            query = """
                SELECT 
                    te.Company_name AS company_name,
                    COUNT(te.TempSsn) AS employee_count,
                    GROUP_CONCAT(DISTINCT e.Name SEPARATOR ', ') AS supervisors
                FROM Temporary_Employee te
                JOIN TempSupervise ts ON te.TempSsn = ts.Supervisee_Ssn_temp_employee
                JOIN Employee e ON ts.Supervisor_Ssn_midlevel_manager = e.Ssn
                GROUP BY te.Company_name
                ORDER BY employee_count DESC
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_vacant_office_distribution(self):
        try:
            db = DatabaseConnection()
            query = """
                SELECT 
                    Office_Building AS building,
                    Office_Floor AS floor,
                    COUNT(Office_RoomNum) AS vacant_count
                FROM Office
                WHERE OwnerSsn IS NULL
                GROUP BY Office_Building, Office_Floor
                ORDER BY Office_Building, Office_Floor
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_supervision_hierarchy(self):
        try:
            db = DatabaseConnection()
            query = """
                SELECT 
                    s.Name AS supervisor_name,
                    s.Emp_Level AS supervisor_level,
                    se.Name AS subordinate_name,
                    se.Emp_Level AS subordinate_level,
                    se.Ssn AS subordinate_id
                FROM Employee_Supervision es
                JOIN Employee s ON es.Supervisor_Ssn = s.Ssn
                JOIN Employee se ON es.Supervisee_Ssn = se.Ssn
                ORDER BY s.Emp_Level DESC, s.Name
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
