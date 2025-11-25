from .connection import DatabaseConnection
from .validators import Validators
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class EmployeeDAO:
    def __init__(self):
        self.connection_pool = DatabaseConnection
    
    def create_employee(self, ssn: str, name: str, emp_level: str) -> Dict[str, Any]:
        try:
            valid, msg = Validators.validate_ssn(ssn)
            if not valid:
                return {"success": False, "error": msg}
            
            valid, msg = Validators.validate_name(name)
            if not valid:
                return {"success": False, "error": msg}
            
            valid, msg = Validators.validate_employee_level(emp_level)
            if not valid:
                return {"success": False, "error": msg}
            
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                INSERT INTO Employee (Ssn, Name, Emp_Level)
                VALUES (%s, %s, %s)
            """
            values = (ssn, name, emp_level)
            
            cursor.execute(query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Employee created successfully: SSN {ssn}")
            return {
                "success": True, 
                "data": {
                    "Ssn": ssn,
                    "Name": name,
                    "Emp_Level": emp_level
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create employee: {str(e)}")
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def get_employee_by_ssn(self, ssn: str) -> Optional[Dict[str, Any]]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Employee WHERE Ssn = %s"
            cursor.execute(query, (ssn,))
            employee = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return employee
            
        except Exception as e:
            logger.error(f"Failed to get employee by SSN {ssn}: {str(e)}")
            return None
    
    def get_all_employees(self) -> List[Dict[str, Any]]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Employee ORDER BY Emp_Level, Name"
            cursor.execute(query)
            employees = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return employees
            
        except Exception as e:
            logger.error(f"Failed to get all employees: {str(e)}")
            return []
    
    def get_employees_by_level(self, emp_level: str) -> List[Dict[str, Any]]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Employee WHERE Emp_Level = %s ORDER BY Name"
            cursor.execute(query, (emp_level,))
            employees = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return employees
            
        except Exception as e:
            logger.error(f"Failed to get employees by level {emp_level}: {str(e)}")
            return []
    
    def get_mid_level_managers(self) -> List[Dict[str, Any]]:
        return self.get_employees_by_level('mid_level manager')
    
    def get_base_level_workers(self) -> List[Dict[str, Any]]:
        return self.get_employees_by_level('base_level worker')
    
    def get_executive_officers(self) -> List[Dict[str, Any]]:
        return self.get_employees_by_level('executive officer')
    
    def update_employee(self, ssn: str, **kwargs) -> Dict[str, Any]:
        try:
            if not kwargs:
                return {"success": False, "error": "No fields to update"}
            
            set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
            values = list(kwargs.values())
            values.append(ssn)
            
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            
            query = f"UPDATE Employee SET {set_clause} WHERE Ssn = %s"
            cursor.execute(query, values)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Employee {ssn} updated successfully")
            return {"success": True, "data": {"Ssn": ssn, **kwargs}}
            
        except Exception as e:
            logger.error(f"Failed to update employee {ssn}: {str(e)}")
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def delete_employee(self, ssn: str) -> Dict[str, Any]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM Employee WHERE Ssn = %s"
            cursor.execute(query, (ssn,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Employee {ssn} deleted successfully")
            return {"success": True, "data": {"Ssn": ssn}}
            
        except Exception as e:
            logger.error(f"Failed to delete employee {ssn}: {str(e)}")
            return {"success": False, "error": f"Database error: {str(e)}"}
