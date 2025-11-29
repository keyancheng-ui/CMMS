
from datetime import datetime, date
from typing import Tuple


class Validators:

    @staticmethod
    # check the validation of employee level
    def validate_employee_level(level):
        valid_levels = ['executive officer', 'mid_level manager', 'base_level worker']
        if level not in valid_levels:
            print(f"Employee level must be in [{valid_levels[0]}, {valid_levels[1]}, {valid_levels[2]}]")
            return False
        return True
    # finished

    @staticmethod
    # check whether two Ssns are distinct
    def ensure_distinct(a, b):
        if a == b:
            print("Two Ssns of a supervision cannot be the same.")
            return False

    @staticmethod
    # check the validation of contractor company name
    def validate_company_name(company_name):
        if not company_name or len(company_name) == 0:
            print("Company name cannot be empty. Input again.")
            return False
        elif len(company_name) > 100:
            print("Company name is too long.")
            return False
        else:
            return True

    @staticmethod
    #手工自制楼名检查函数
    def validate_building(building) -> Tuple[bool, str]:
        if not building or len(building.strip()) == 0:
            return False, "Building cannot be empty"
        if len(building) > 20:
            return False, "Building name must not exceed 20 characters"
        return True, "Building Insertion Succeeded"

    @staticmethod
    # 手工自制层数检查函数（只能为非负整数）
    def validate_floor(floor) -> Tuple[bool, str]:
        if floor < 0:
            return False,
        if not isinstance(floor, int):
            return False, "Floor must be an integer"
        return True, "Floor Insertion Succeeded"

    @staticmethod
    # 手工自制房号检查函数
    def validate_room(room) -> Tuple[bool, str]:
        if room <= 0:
            return False, "Room number must be positive"
        if room <= 100:
            return False, "Room number must be greater than 100"
        if not isinstance(room, int):
            return False, "Floor must be an integer"
        return True, "Valid room number"















    @staticmethod
    def validate_activity_type(activity_type: str) -> Tuple[bool, str]:
        valid_types = ['daily campus cleaning', 'campus ageing', 'weather-related issues']
        if activity_type not in valid_types:
            return False, f"Activity type must be one of: {', '.join(valid_types)}"
        return True, "Valid activity type"

    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, "Valid date"
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"



    @staticmethod
    def validate_applied_reason(reason: str) -> Tuple[bool, str]:
        if not reason or len(reason.strip()) == 0:
            return False, "Applied reason cannot be empty"
        if len(reason) > 100:
            return False, "Applied reason must not exceed 100 characters"
        return True, "Valid applied reason"

    @staticmethod
    def validate_not_empty(field_name: str, value: str) -> Tuple[bool, str]:
        if not value or not str(value).strip():
            return False, f"{field_name} cannot be empty"
        return True, f"Valid {field_name}"

    @staticmethod
    def validate_ids_not_equal(id1: str, id2: str, field1: str, field2: str) -> Tuple[bool, str]:
        if id1 == id2:
            return False, f"{field1} and {field2} cannot be the same"
        return True, "IDs are different"

    @staticmethod
    def validate_chemical_requirement(require_chemical: int) -> Tuple[bool, str]:
        if require_chemical not in [0, 1]:
            return False, "Require_Chemical must be 0 or 1"
        return True, "Valid chemical requirement"

    def validate_date(date_str: str) -> None:
        ok, msg = Validators.validate_date(date_str)
        if not ok:
            raise ValueError(msg)

def ensure_not_empty(value: str) -> None:
        if not value or not str(value).strip():
            raise ValueError("value cannot be empty")


