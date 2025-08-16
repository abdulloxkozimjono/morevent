from django.core.exceptions import ValidationError
import re


def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError("Username faqat harf, raqam va _ belgisidan iborat bo‘lishi mumkin.")
    if len(value) < 3:
        raise ValidationError("Username kamida 3 ta belgidan iborat bo‘lishi kerak.")
    return value


def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")
    if not re.search(r'[A-Z]', value):
        raise ValidationError("Parolda kamida 1 ta katta harf bo‘lishi kerak.")
    if not re.search(r'[a-z]', value):
        raise ValidationError("Parolda kamida 1 ta kichik harf bo‘lishi kerak.")
    if not re.search(r'[0-9]', value):
        raise ValidationError("Parolda kamida 1 ta raqam bo‘lishi kerak.")
    return value
