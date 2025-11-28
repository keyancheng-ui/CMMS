from .connection import DatabaseConnection
from .validators import Validators, ensure_not_empty

class TempEmployeeDAO:
    def __init__(self):
        pass

    def create_temp_employee(self, temp_ssn, company_name):
        try:
            ensure_not_empty(temp_ssn)
            ensure_not_empty(company_name)
            
            valid, msg = Validators.validate_ssn(temp_ssn)
            if not valid:
                return {"success": False, "error": msg}
                
            valid, msg = Validators.validate_company_name(company_name)
            if not valid:
                return {"success": False, "error": msg}

            db = DatabaseConnection()
            query = "INSERT INTO Temporary_Employee (TempSsn, Company_name) VALUES (%s, %s)"
            
            cursor = db.connection.cursor()
            cursor.execute(query, (temp_ssn, company_name))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {"TempSsn": temp_ssn, "Company_name": company_name}}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_temp_employee_by_ssn(self, temp_ssn):
        try:
            ensure_not_empty(temp_ssn)
            
            db = DatabaseConnection()
            query = "SELECT * FROM Temporary_Employee WHERE TempSsn = %s"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (temp_ssn,))
            result = cursor.fetchone()
            cursor.close()
            db.close()
            
            if result:
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": "Temp employee not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_temp_employees(self):
        try:
            db = DatabaseConnection()
            query = "SELECT * FROM Temporary_Employee ORDER BY Company_name, TempSsn"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}


