from .connection import DatabaseConnection
from .validators import Validators
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ContractorDAO:
    def __init__(self):
        self.connection_pool = DatabaseConnection
    
    def create_contractor_company(self, temp_employee_ssn: str, name: str) -> Dict[str, Any]:
        try:
            valid, msg = Validators.validate_ssn(temp_employee_ssn)
            if not valid:
                return {"success": False, "error": msg}
            
            valid, msg = Validators.validate_company_name(name)
            if not valid:
                return {"success": False, "error": msg}
            
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                INSERT INTO Contractor_Company (Temp_Employee_Ssn, name)
                VALUES (%s, %s)
            """
            values = (temp_employee_ssn, name)
            
            cursor.execute(query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Contractor company created successfully for temp employee {temp_employee_ssn}")
            return {
                "success": True, 
                "data": {
                    "Temp_Employee_Ssn": temp_employee_ssn,
                    "name": name
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create contractor company: {str(e)}")
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def get_contractor_by_temp_employee_ssn(self, temp_employee_ssn: str) -> Optional[Dict[str, Any]]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Contractor_Company WHERE Temp_Employee_Ssn = %s"
            cursor.execute(query, (temp_employee_ssn,))
            contractor = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return contractor
            
        except Exception as e:
            logger.error(f"Failed to get contractor by temp employee SSN {temp_employee_ssn}: {str(e)}")
            return None
    
    def get_all_contractors(self) -> List[Dict[str, Any]]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT cc.*, te.Company_name 
                FROM Contractor_Company cc
                JOIN Temporary_Employee te ON cc.Temp_Employee_Ssn = te.TempSsn
                ORDER BY cc.name
            """
            cursor.execute(query)
            contractors = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return contractors
            
        except Exception as e:
            logger.error(f"Failed to get all contractors: {str(e)}")
            return []
    
    def update_contractor(self, temp_employee_ssn: str, **kwargs) -> Dict[str, Any]:
        try:
            if not kwargs:
                return {"success": False, "error": "No fields to update"}
            
            set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
            values = list(kwargs.values())
            values.append(temp_employee_ssn)
            
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            
            query = f"UPDATE Contractor_Company SET {set_clause} WHERE Temp_Employee_Ssn = %s"
            cursor.execute(query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Contractor {temp_employee_ssn} updated successfully")
            return {"success": True, "data": {"Temp_Employee_Ssn": temp_employee_ssn, **kwargs}}
            
        except Exception as e:
            logger.error(f"Failed to update contractor {temp_employee_ssn}: {str(e)}")
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def delete_contractor(self, temp_employee_ssn: str) -> Dict[str, Any]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM Contractor_Company WHERE Temp_Employee_Ssn = %s"
            cursor.execute(query, (temp_employee_ssn,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Contractor {temp_employee_ssn} deleted successfully")
            return {"success": True, "data": {"Temp_Employee_Ssn": temp_employee_ssn}}
            
        except Exception as e:
            logger.error(f"Failed to delete contractor {temp_employee_ssn}: {str(e)}")
            return {"success": False, "error": f"Database error: {str(e)}"}
