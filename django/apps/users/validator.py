# validators.py
import re
from django.core.exceptions import ValidationError


def validate_uzbekistan_phone(value):
    pattern = re.compile(r'^\+998\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$')
    if not pattern.match(value):
        raise ValidationError(message='Invalid Uzbekistan phone number format.')
