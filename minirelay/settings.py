import os
from decouple import config

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

SQLITE_STORE = config("SQLITE_STORE")
BASE_DOMAIN = config("DOMAIN")
SENDGRID_API_KEY = config("SENDGRID_API_KEY")
MAIL_EXTENSION = "@" + BASE_DOMAIN
FROM_EMAIL = config("FROM_EMAIL")
ENGINE = create_engine(f'sqlite:///{SQLITE_STORE}', echo=True)
SESSION = Session(ENGINE)
