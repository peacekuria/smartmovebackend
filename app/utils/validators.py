import re


def validate_email(email):
    """Validates email format."""
    pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return bool(pattern.match(email))


def validate_kenyan_phone(phone):
    """
    Validates Safaricom, Airtel, Telkom numbers.
    Formats accepted: +254..., 07..., 01...
    """
    pattern = re.compile(r"^(?:\+254|0)[17]\d{8}$")
    return bool(pattern.match(str(phone)))


def validate_password_strength(password):
    """Ensures password is at least 8 characters."""
    return len(password) >= 8
