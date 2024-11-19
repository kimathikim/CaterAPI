# utils/validators.py

import re


def validate_email(email):
    """Validates if the email follows a valid format"""
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email) is not None


def validate_password_strength(password):
    """Validates password strength"""
    if len(password) < 6:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    return True


def validate_guest_count(guest_count):
    """Validates if guest count is a positive number"""
    return guest_count > 0
