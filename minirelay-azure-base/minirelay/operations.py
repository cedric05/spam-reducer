__all__ = ["registerEmail", "generateEmail", "listEmail", "check_email_exists", "enableEmail", "setup"]

import string

from .models import User, Filters
from .exceptions import InValidEmail, AlreadyRegistered, EmailNotGenerated, NotRegistered, SQLException
from .utils import validate_email
from mongoengine.errors import *




def setup():
    # mongodb takes care of creating table itself
    pass


def registerEmail(email_address):
    if not validate_email(email_address):
        raise InValidEmail("email is not valid")
    try:
        user = User()
        user.email_address=email_address
        user.save(force_insert=True)
    except NotUniqueError as e:
        raise AlreadyRegistered("email already registered", e)


def generateEmail(email_address, extra_or_site="") -> str:
    check_email_exists(email_address)
    filter = Filters()
    filter.email_address = email_address
    filter.site = extra_or_site
    filter.save()
    return filter.generated



def enableEmail(generated, enable=True):
    Filters.objects(generated=generated).update(enabled=enable)

def listEmail(email_address: object) -> object:
    validate_email(email_address)
    check_email_exists(email_address)
    all_filters = Filters.objects(email_address=email_address)
    result = {"email": email_address}
    filters = []
    result["filters"] = filters
    try:
        for filter_data in all_filters:
            filters.append(
                {"generated": filter_data.generated, "enabled": filter_data.enabled, "site": filter_data.site})
        return result
    except (DoesNotExist, LookUpError):
        return result


def check_email_exists(email_address):
    query_result = User.objects(email_address = email_address).limit(1)
    if not query_result:
        raise NotRegistered(f"email {email_address} not registered ")


def get_original_email(generated: str):
    query = Filters.objects(generated=generated).limit(1)
    if query and query[0].enabled:
        return query[0]
    else:
        raise DisabledEmail("unknown generated email!! or not at all registered")

