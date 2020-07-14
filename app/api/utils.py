import re


def verify_user_update_fields(**kwargs) -> (bool, str, int):
    for k, v in kwargs.items():
        if k == "username":
            if bool(re.search('[a-zA-Z]', k)):
                return False, "You cannot have an empty username.", 400
