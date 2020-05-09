from decouple import config

from mongoengine import connect

BASE_DOMAIN = config("DOMAIN")
SENDGRID_API_KEY = config("SENDGRID_API_KEY")
MAIL_EXTENSION = "@" + BASE_DOMAIN