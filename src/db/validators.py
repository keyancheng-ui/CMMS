from datetime import datetime
from typing import Tuple


class Validators:

    # ------ these are all functions to check validation for all input about "activity" ------

    # 1. check the validation of activity type
    @staticmethod
    def validate_activity_type(activity_type):
        valid_types = ['daily campus cleaning', 'campus ageing', 'weather-related issues']
        if activity_type not in valid_types:
            return False
        return True
    # finished

    # 2. check the validation of activity time
    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    # finished

    # 3. check the validation of floor number
    @staticmethod
    def validate_floor(floor):
        if int(floor) < 0:
            return False
        return True
    # finished

    # 4. check the validation of room number
    @staticmethod
    def validate_room(room):
        if int(room) <= 100:
            return False
        return True
    # finished

    # 5. check the validation of chemical required condition
    @staticmethod
    def validate_chemical_requirement(require_chemical):
        if int(require_chemical) not in [0, 1]:
            return False
        return True
    # finished

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




