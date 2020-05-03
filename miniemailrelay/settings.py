import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

SQLITE_STORE = os.environ.get("SQLITE_STORE", "test.db")
BASE_DOMAIN = os.environ.get("DOMAIN", "mailtest.prasanth.info")
MAIL_EXTENSION = "@" + BASE_DOMAIN
engine = create_engine(f'sqlite:///{SQLITE_STORE}', echo=True)
session = Session(engine)