import re
from datetime import datetime, date
from typing import Tuple

class Validators:
    @staticmethod
    def validate_ssn(ssn: str) -> Tuple[bool, str]:
        if not ssn or len(ssn.strip()) == 0:
            return False, "SSN cannot be empty"
        if len(ssn) > 20:
            return False, "SSN must not exceed 20 characters"
        return True, "Valid SSN"

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        if not name or len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long"
        if len(name) > 100:
            return False, "Name must not exceed 100 characters"
        return True, "Valid name"

    @staticmethod
    def validate_employee_level(level: str) -> Tuple[bool, str]:
        valid_levels = ['executive officer', 'mid_level manager', 'base_level worker']
        if level not in valid_levels:
            return False, f"Employee level must be one of: {', '.join(valid_levels)}"
        return True, "Valid employee level"

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
    def validate_building(building: str) -> Tuple[bool, str]:
        if not building or len(building.strip()) == 0:
            return False, "Building cannot be empty"
        if len(building) > 20:
            return False, "Building name must not exceed 20 characters"
        return True, "Valid building"

    @staticmethod
    def validate_floor(floor: int) -> Tuple[bool, str]:
        if floor < 0:
            return False, "Floor cannot be negative"
        return True, "Valid floor"

    @staticmethod
    def validate_room(room: int) -> Tuple[bool, str]:
        if room <= 0:
            return False, "Room number must be positive"
        return True, "Valid room number"

    @staticmethod
    def validate_company_name(company: str) -> Tuple[bool, str]:
        if not company or len(company.strip()) == 0:
            return False, "Company name cannot be empty"
        if len(company) > 100:
            return False, "Company name must not exceed 100 characters"
        return True, "Valid company name"

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

def ensure_distinct(a: str, b: str) -> None:
    if a == b:
        raise ValueError("values must be distinct")
