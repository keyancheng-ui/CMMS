from .connection import DatabaseConnection
from .validators import Validators, ensure_not_empty

class EmployeeDAO:
    def __init__(self):
        pass

    def create_employee(self, ssn, name, emp_level):
        try:
            ensure_not_empty(ssn)
            ensure_not_empty(name)
            ensure_not_empty(emp_level)
            
            valid, msg = Validators.validate_ssn(ssn)
            if not valid:
                return {"success": False, "error": msg}
                
            valid, msg = Validators.validate_name(name)
            if not valid:
                return {"success": False, "error": msg}
                
            valid, msg = Validators.validate_employee_level(emp_level)
            if not valid:
                return {"success": False, "error": msg}

            db = DatabaseConnection()
            query = "INSERT INTO Employee (Ssn, Name, Emp_Level) VALUES (%s, %s, %s)"
            
            cursor = db.connection.cursor()
            cursor.execute(query, (ssn, name, emp_level))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {"Ssn": ssn, "Name": name, "Emp_Level": emp_level}}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_employee_by_ssn(self, ssn):
        try:
            ensure_not_empty(ssn)
            
            db = DatabaseConnection()
            query = "SELECT * FROM Employee WHERE Ssn = %s"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (ssn,))
            result = cursor.fetchone()
            cursor.close()
            db.close()
            
            if result:
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": "Employee not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_employees(self):
        try:
            db = DatabaseConnection()
            query = "SELECT * FROM Employee ORDER BY Emp_Level, Name"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_employee(self, ssn, name=None, emp_level=None):
        try:
            ensure_not_empty(ssn)
            
            updates = []
            params = []
            
            if name is not None:
                valid, msg = Validators.validate_name(name)
                if not valid:
                    return {"success": False, "error": msg}
                updates.append("Name = %s")
                params.append(name)
                
            if emp_level is not None:
                valid, msg = Validators.validate_employee_level(emp_level)
                if not valid:
                    return {"success": False, "error": msg}
                updates.append("Emp_Level = %s")
                params.append(emp_level)
                
            if not updates:
                return {"success": False, "error": "No fields to update"}
                
            params.append(ssn)
            set_clause = ", ".join(updates)
            query = f"UPDATE Employee SET {set_clause} WHERE Ssn = %s"
            
            db = DatabaseConnection()
            cursor = db.connection.cursor()
            cursor.execute(query, params)
            db.connection.commit()
            affected = cursor.rowcount
            cursor.close()
            db.close()
            
            if affected > 0:
                return {"success": True, "data": {"Ssn": ssn, "updated_fields": updates}}
            else:
                return {"success": False, "error": "Employee not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_employee(self, ssn):
        try:
            ensure_not_empty(ssn)
            
            db = DatabaseConnection()
            query = "DELETE FROM Employee WHERE Ssn = %s"
            
            cursor = db.connection.cursor()
            cursor.execute(query, (ssn,))
            db.connection.commit()
            affected = cursor.rowcount
            cursor.close()
            db.close()
            
            if affected > 0:
                return {"success": True, "data": {"Ssn": ssn}}
            else:
                return {"success": False, "error": "Employee not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
