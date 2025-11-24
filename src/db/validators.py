import os
from datetime import datetime

def validate_date(date_str: str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        raise ValueError("invalid date format")
    base = os.getenv("SYSTEM_CREATION_DATE")
    if base:
        b = datetime.strptime(base, "%Y-%m-%d")
        if d < b:
            raise ValueError("date earlier than system creation date")

def ensure_not_empty(value: str):
    if value is None or str(value).strip() == "":
        raise ValueError("empty value")

def ensure_distinct(a, b):
    if a == b:
        raise ValueError("ids must be distinct")
