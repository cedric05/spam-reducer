import string

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from .exceptions import InValidEmail, AlreadyRegistered, EmailNotGenerated, NotRegistered
from .settings import session
from .models import User, Filters
from .utils import validate_email


def registerEmail(email):
    if not validate_email(email):
        raise InValidEmail("email is not valid")
    try:
        user = User()
        user.email = email
        session.add(user)
        session.commit()
    except IntegrityError:
        raise AlreadyRegistered("email already registered")


def generateEmail(email, extra_or_site=""):
    check_email_exists(email)
    filter = Filters()
    filter.email = email
    filter.site = extra_or_site
    session.add_all([filter])
    session.commit()
    return True


def enableEmail(email, generated, enable=True):
    check_email_exists(email)
    query_result = session.query(Filters).filter(Filters.generated == generated)
    try:
        first = query_result.first()
    except NoResultFound:
        raise EmailNotGenerated("email not generated")
    if enable:
        first.enabled = True
    else:
        first.enabled = False
    session.commit()


def listEmail(email: string) -> object:
    validate_email(email)
    check_email_exists(email)
    query_result = session.query(Filters).filter(Filters.email == email)
    result = {"email": email}
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


def check_email_exists(email):
    query_result = session.query(User).filter(User.email == email)
    try:
        result = query_result.first()
    except NoResultFound:
        raise NotRegistered("email not registered")