import re


def validate_email(email):
    if (re.search(regex, email)):
        return True
    else:
        return False


regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'