from re import fullmatch

from soon import StringValueObject
from soon.exceptions import Invalid


class Email(StringValueObject):
    def validate(self):
        if not fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", self):
            raise Invalid("Invalid email.")
