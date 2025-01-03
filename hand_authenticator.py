from hand_side import HandSide
from password_status import PasswordStatus

SECRET_PASSWORD = [HandSide.RIGHT, HandSide.RIGHT, HandSide.LEFT]


def verify_password(hands_motions: list[HandSide]) -> PasswordStatus:
    if SECRET_PASSWORD == hands_motions[:len(SECRET_PASSWORD)]:
        return PasswordStatus.MATCH
    elif SECRET_PASSWORD[:len(hands_motions)] == hands_motions:
        return PasswordStatus.IN_PROCESS
    else:
        return PasswordStatus.NOT_MATCH
