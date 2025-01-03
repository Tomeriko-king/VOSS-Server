from enum import Enum


class PasswordStatus(Enum):
    MATCH = b'MATCH'
    NOT_MATCH = b'NOT_MATCH'
    IN_PROCESS = b'IN_PROCESS'
