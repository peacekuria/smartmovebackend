import uuid
from datetime import datetime


def generate_unique_id():
    return str(uuid.uuid4())


def generate_booking_ref():
    """Generates a short human-readable reference (e.g., SM-2024-X89)"""
    year = datetime.now().year
    random_part = str(uuid.uuid4()).upper()[:4]
    return f"SM-{year}-{random_part}"


def format_currency(amount):
    return f"KES {amount:,.2f}"
from datetime import datetime

def format_date(date_obj, format_string="%Y-%m-%d %H:%M:%S"):
    """
    Formats a datetime object into a string.
    """
    if not isinstance(date_obj, datetime):
        return None
    return date_obj.strftime(format_string)

def generate_random_string(length=10):
    """
    Generates a random string of specified length.
    """
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
