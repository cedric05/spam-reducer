import re
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
import os
import random, string

from sqlalchemy.orm.exc import NoResultFound

SQLITE_STORE = os.environ.get("SQLITE_STORE", "test.db")
BASE_DOMAIN = os.environ.get("DOMAIN", "mailtest.prasanth.info")
MAIL_EXTENSION = "@" + BASE_DOMAIN

engine = create_engine(f'sqlite:///{SQLITE_STORE}', echo=True)
session = Session(engine)
Base = declarative_base()


def address_default():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9)) + MAIL_EXTENSION


class User(Base):
    __tablename__ = "users"
    email = Column(String(120), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return '<User %r>' % self.email


class Filters(Base):
    __tablename__ = "filters"
    email = Column(String(120), unique=True, nullable=False)
    generated = Column(String(120), unique=True, nullable=False, primary_key=True, default=address_default)
    enabled = Column(Boolean(), unique=True, nullable=False, default=True)
    site = Column(String(120), nullable=True)


regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


class SpamReducerException(Exception):
    pass


class InValidEmail(SpamReducerException):
    pass


class NotRegistered(SpamReducerException):
    pass


class AlreadyRegistered(SpamReducerException):
    pass


class NotGeneratedEmail(SpamReducerException):
    pass


class SQLException(SpamReducerException):
    pass


class EmailNotGenerated(SpamReducerException):
    pass


def validate_email(email):
    if (re.search(regex, email)):
        return True
    else:
        return False


def check_email_exists(email):
    query_result = session.query(User).filter(User.email == email)
    try:
        result = query_result.first()
    except NoResultFound:
        raise NotRegistered("email not registered")


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
