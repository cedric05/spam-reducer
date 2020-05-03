import random
import string

from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from .settings import MAIL_EXTENSION

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
