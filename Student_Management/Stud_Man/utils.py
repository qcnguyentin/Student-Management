from flask_login import current_user

from Stud_Man.models import UserRole


def check_user_role():
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.TEACHER:
            user_role = 1
        elif current_user.user_role == UserRole.EMPLOYEE:
            user_role = 2
        else:
            user_role = 3
    else:
        user_role = 0
    return user_role
