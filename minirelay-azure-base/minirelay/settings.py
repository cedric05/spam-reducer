from decouple import config

from mongoengine import connect

connect("minirelay", host=config("MONGO_HOST", default="mongodb://localhost:27017/minirelay"))
BASE_DOMAIN = config("DOMAIN")
SENDGRID_API_KEY = config("SENDGRID_API_KEY")
MAIL_EXTENSION = "@" + BASE_DOMAIN