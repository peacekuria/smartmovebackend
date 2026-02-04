import re

class Validator:
    @staticmethod
    def is_valid_email(email):
        """
        Validates if the given string is a valid email format.
        """
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    @staticmethod
    def is_strong_password(password):
        """
        Validates if the given password meets basic strength requirements:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        - Contains at least one special character
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
            return False
        return True

    @staticmethod
    def is_not_empty(value, field_name="Field"):
        """
        Checks if a value is not None and not an empty string/list/dict.
        """
        if value is None:
            return False, f"{field_name} cannot be empty."
        if isinstance(value, str) and not value.strip():
            return False, f"{field_name} cannot be empty."
        if isinstance(value, (list, dict)) and not value:
            return False, f"{field_name} cannot be empty."
        return True, ""

    @staticmethod
    def validate_required_fields(data, required_fields):
        """
        Validates that all required fields are present in the data dictionary.
        Returns (True, "") if all fields are present, otherwise (False, error_message).
        """
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        return True, ""