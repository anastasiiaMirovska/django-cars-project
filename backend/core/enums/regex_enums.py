from enum import Enum


class RegexEnum(Enum):
    NAME = (
        r'^[A-Z][a-zA-Z]{1,19}$',
        'First letter uppercase, min 2, max 20'
    )
    PASSWORD = (
        r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])(\S){8,18}$',
        [
            'Password must contain at least 1 number (1-9)',
            'Password must contain at least 1 uppercase letter',
            'Password must contain at least 1 lowercase letter',
            'Password must contain at least 1 special character',
            'Password must contain min 8 max 16 characters without spaces'
        ]
    )
    PHONE = (
        r'^\+380(39|50|63|66|67|68|73|91|92|93|94|95|96|97|98|99)\d{7}$',
        [
            'Phone number must start with +380',
            'Phone number must contain a valid operator code (39, 50, 63, 66, 67, 68, 73, 91, 92, 93, 94, 95, 96, 97, 98, 99)',
            'Phone number must contain exactly 7 digits after the operator code'
        ]
    )

    def __init__(self, pattern: str, msg: str | list[str]):
        self.pattern = pattern
        self.msg = msg
