from datetime import datetime

def format_datetime(dt):
    """Formats a datetime object to ISO 8601 string format"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return None

def parse_datetime(dt_str):
    """Parses an ISO 8601 string to a datetime object"""
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        return None

