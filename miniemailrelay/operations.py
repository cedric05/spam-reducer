__all__ = ["registerEmail", "generateEmail", "listEmail", "check_email_exists"]

import string

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from .exceptions import InValidEmail, AlreadyRegistered, EmailNotGenerated, NotRegistered
from .models import User, Filters
from .settings import SESSION
from .utils import validate_email


def registerEmail(email_address):
    if not validate_email(email_address):
        raise InValidEmail("email is not valid")
    try:
        user = User()
        user.email_address = email_address
        SESSION.add(user)
        SESSION.commit()
    except IntegrityError:
        raise AlreadyRegistered("email already registered")


def generateEmail(email_address, extra_or_site=""):
    check_email_exists(email_address)
    filter = Filters()
    filter.email_addresss = email_address
    filter.site = extra_or_site
    SESSION.add_all([filter])
    SESSION.commit()
    return filter.generated


def enableEmail(generated, enable=True):
    query_result = SESSION.query(Filters).filter(Filters.generated == generated)
    try:
        first = query_result.first()
    except NoResultFound:
        raise EmailNotGenerated("email not generated")
    if enable:
        first.enabled = True
    else:
        first.enabled = False
    SESSION.commit()


def listEmail(email_address: string) -> object:
    validate_email(email_address)
    check_email_exists(email_address)
    query_result = SESSION.query(Filters).filter(Filters.email_addresss == email_address)
    result = {"email": email_address}
    filters = []
    result["filters"] = filters
    try:
        all_filters = query_result.all()
        for filter_data in all_filters:
            filters.append(
                {"generated": filter_data.generated, "enabled": filter_data.enabled, "site": filter_data.site})
        return result
    except NoResultFound:
        return result


def check_email_exists(email_address):
    query_result = SESSION.query(User).filter(User.email_address == email_address)
    try:
        result = query_result.first()
    except NoResultFound:
        raise NotRegistered("email not registered")


def get_original_email(generated: str) -> str:
    query = SESSION.query(Filters).filter(Filters.generated == generated)
    try:
        first: Filters = query.first()
        if first.enabled:
            return first.email_addresss
    except NoResultFound:
        raise EmailNotGenerated("unknown generated email!!")
