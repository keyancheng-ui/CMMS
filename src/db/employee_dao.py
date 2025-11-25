from .connection import DatabaseConnection
from .validators import Validators
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TempEmployeeDAO:
    def __init__(self):
        self.connection_pool = DatabaseConnection
    
    def create_temp_employee(self, temp_ssn: str, company_name: str) -> Dict[str, Any]:
        try:
            valid, msg = Validators.validate_ssn(temp_ssn)
            if not valid:
                return {"success": False, "error": msg}
            
            valid, msg = Validators.validate_company_name(company_name)
            if not valid:
                return {"success": False, "error": msg}
            
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                INSERT INTO Temporary_Employee (TempSsn, Company_name)
                VALUES (%s, %s)
            """
            values = (temp_ssn, company_name)
            
            cursor.execute(query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Temp employee created successfully: SSN {temp_ssn}")
            return {
                "success": True, 
                "data": {
                    "TempSsn": temp_ssn,
                    "Company_name": company_name
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create temp employee: {str(e)}")
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def get_temp_employee_by_ssn(self, temp_ssn: str) -> Optional[Dict[str, Any]]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Temporary_Employee WHERE TempSsn = %s"
            cursor.execute(query, (temp_ssn,))
            temp_employee = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return temp_employee
            
        except Exception as e:
            logger.error(f"Failed to get temp employee by SSN {temp_ssn}: {str(e)}")
            return None
    
    def get_all_temp_employees(self) -> List[Dict[str, Any]]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Temporary_Employee ORDER BY Company_name, TempSsn"
            cursor.execute(query)
            temp_employees = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return temp_employees
            
        except Exception as e:
            logger.error(f"Failed to get all temp employees: {str(e)}")
            return []
    
    def get_temp_employees_by_company(self, company_name: str) -> List[Dict[str, Any]]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Temporary_Employee WHERE Company_name LIKE %s ORDER BY TempSsn"
            cursor.execute(query, (f"%{company_name}%",))
            temp_employees = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return temp_employees
            
        except Exception as e:
            logger.error(f"Failed to get temp employees by company {company_name}: {str(e)}")
            return []
    
    def update_temp_employee(self, temp_ssn: str, **kwargs) -> Dict[str, Any]:
        try:
            if not kwargs:
                return {"success": False, "error": "No fields to update"}
            
            set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
            values = list(kwargs.values())
            values.append(temp_ssn)
            
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            
            query = f"UPDATE Temporary_Employee SET {set_clause} WHERE TempSsn = %s"
            cursor.execute(query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Temp employee {temp_ssn} updated successfully")
            return {"success": True, "data": {"TempSsn": temp_ssn, **kwargs}}
            
        except Exception as e:
            logger.error(f"Failed to update temp employee {temp_ssn}: {str(e)}")
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def delete_temp_employee(self, temp_ssn: str) -> Dict[str, Any]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM Temporary_Employee WHERE TempSsn = %s"
            cursor.execute(query, (temp_ssn,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Temp employee {temp_ssn} deleted successfully")
            return {"success": True, "data": {"TempSsn": temp_ssn}}
            
        except Exception as e:
            logger.error(f"Failed to delete temp employee {temp_ssn}: {str(e)}")
            return {"success": False, "error": f"Database error: {str(e)}"}
