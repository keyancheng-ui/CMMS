from .connection import DatabaseConnection
from .validators import Validators, ensure_not_empty

class ContractorDAO:
    def __init__(self):
        pass

    def create_contractor_company(self, temp_employee_ssn, name):
        try:
            ensure_not_empty(temp_employee_ssn)
            ensure_not_empty(name)
            
            valid, msg = Validators.validate_ssn(temp_employee_ssn)
            if not valid:
                return {"success": False, "error": msg}
                
            valid, msg = Validators.validate_company_name(name)
            if not valid:
                return {"success": False, "error": msg}

            db = DatabaseConnection()
            query = "INSERT INTO Contractor_Company (Temp_Employee_Ssn, name) VALUES (%s, %s)"
            
            cursor = db.connection.cursor()
            cursor.execute(query, (temp_employee_ssn, name))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {"Temp_Employee_Ssn": temp_employee_ssn, "name": name}}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_contractor_by_temp_employee_ssn(self, temp_employee_ssn):
        try:
            ensure_not_empty(temp_employee_ssn)
            
            db = DatabaseConnection()
            query = "SELECT * FROM Contractor_Company WHERE Temp_Employee_Ssn = %s"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (temp_employee_ssn,))
            result = cursor.fetchone()
            cursor.close()
            db.close()
            
            if result:
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": "Contractor not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_contractors(self):
        try:
            db = DatabaseConnection()
            query = "SELECT * FROM Contractor_Company ORDER BY name"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}from .connection import DatabaseConnection
from .validators import Validators, ensure_not_empty

class ContractorDAO:
    def __init__(self):
        pass

    def create_contractor_company(self, temp_employee_ssn, name):
        try:
            ensure_not_empty(temp_employee_ssn)
            ensure_not_empty(name)
            
            valid, msg = Validators.validate_ssn(temp_employee_ssn)
            if not valid:
                return {"success": False, "error": msg}
                
            valid, msg = Validators.validate_company_name(name)
            if not valid:
                return {"success": False, "error": msg}

            db = DatabaseConnection()
            query = "INSERT INTO Contractor_Company (Temp_Employee_Ssn, name) VALUES (%s, %s)"
            
            cursor = db.connection.cursor()
            cursor.execute(query, (temp_employee_ssn, name))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {"Temp_Employee_Ssn": temp_employee_ssn, "name": name}}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_contractor_by_temp_employee_ssn(self, temp_employee_ssn):
        try:
            ensure_not_empty(temp_employee_ssn)
            
            db = DatabaseConnection()
            query = "SELECT * FROM Contractor_Company WHERE Temp_Employee_Ssn = %s"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (temp_employee_ssn,))
            result = cursor.fetchone()
            cursor.close()
            db.close()
            
            if result:
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": "Contractor not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_contractors(self):
        try:
            db = DatabaseConnection()
            query = "SELECT * FROM Contractor_Company ORDER BY name"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
