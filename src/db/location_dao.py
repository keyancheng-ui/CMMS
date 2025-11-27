from .connection import DatabaseConnection
from .validators import Validators, ensure_not_empty

class LocationDAO:
    def __init__(self):
        pass

    def create_location(self, building, floor, room_number):
        try:
            ensure_not_empty(building)

            valid, msg = Validators.validate_building(building)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_floor(floor)
            if not valid:
                return {"success": False, "error": msg}

            valid, msg = Validators.validate_room(room_number)
            if not valid:
                return {"success": False, "error": msg}

            db = DatabaseConnection()
            query = "INSERT INTO Location (Building, Floor, Room_number) VALUES (%s, %s, %s)"
            
            cursor = db.connection.cursor()
            cursor.execute(query, (building, floor, room_number))
            db.connection.commit()
            cursor.close()
            db.close()
            
            return {"success": True, "data": {
                "Building": building,
                "Floor": floor,
                "Room_number": room_number
            }}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_location(self, building, floor, room_number):
        try:
            ensure_not_empty(building)

            db = DatabaseConnection()
            query = "SELECT * FROM Location WHERE Building = %s AND Floor = %s AND Room_number = %s"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (building, floor, room_number))
            result = cursor.fetchone()
            cursor.close()
            db.close()
            
            if result:
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": "Location not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_locations(self):
        try:
            db = DatabaseConnection()
            query = "SELECT * FROM Location ORDER BY Building, Floor, Room_number"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_locations_by_building(self, building):
        try:
            ensure_not_empty(building)

            db = DatabaseConnection()
            query = "SELECT * FROM Location WHERE Building = %s ORDER BY Floor, Room_number"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (building,))
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_offices_by_owner(self, owner_ssn):
        try:
            ensure_not_empty(owner_ssn)

            db = DatabaseConnection()
            query = """
                SELECT o.*, e.Name as OwnerName
                FROM Office o
                LEFT JOIN Employee e ON o.OwnerSsn = e.Ssn
                WHERE o.OwnerSsn = %s
                ORDER BY o.Office_Building, o.Office_Floor, o.Office_RoomNum
            """
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query, (owner_ssn,))
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_vacant_offices(self):
        try:
            db = DatabaseConnection()
            query = "SELECT * FROM Office WHERE OwnerSsn IS NULL ORDER BY Office_Building, Office_Floor, Office_RoomNum"
            
            cursor = db.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            db.close()
            
            return {"success": True, "data": results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def assign_office_to_employee(self, building, floor, room_num, owner_ssn):
        try:
            ensure_not_empty(building)
            ensure_not_empty(owner_ssn)

            db = DatabaseConnection()
            query = """
                UPDATE Office 
                SET OwnerSsn = %s 
                WHERE Office_Building = %s AND Office_Floor = %s AND Office_RoomNum = %s
            """
            
            cursor = db.connection.cursor()
            cursor.execute(query, (owner_ssn, building, floor, room_num))
            db.connection.commit()
            affected = cursor.rowcount
            cursor.close()
            db.close()
            
            if affected > 0:
                return {"success": True, "data": {
                    "Office_Building": building,
                    "Office_Floor": floor,
                    "Office_RoomNum": room_num,
                    "OwnerSsn": owner_ssn
                }}
            else:
                return {"success": False, "error": "Office not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}

    def vacate_office(self, building, floor, room_num):
        try:
            ensure_not_empty(building)

            db = DatabaseConnection()
            query = """
                UPDATE Office 
                SET OwnerSsn = NULL 
                WHERE Office_Building = %s AND Office_Floor = %s AND Office_RoomNum = %s
            """
            
            cursor = db.connection.cursor()
            cursor.execute(query, (building, floor, room_num))
            db.connection.commit()
            affected = cursor.rowcount
            cursor.close()
            db.close()
            
            if affected > 0:
                return {"success": True, "data": {
                    "Office_Building": building,
                    "Office_Floor": floor,
                    "Office_RoomNum": room_num
                }}
            else:
                return {"success": False, "error": "Office not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
