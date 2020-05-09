import random
import string
from mongoengine import *
from .settings import *




def address_default():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9)) + MAIL_EXTENSION


class User(Document):
    email_address = StringField(null=False, primary_key=True)
    name = StringField(default="prasanthrocks") # not needed mongoengine fault

    def __repr__(self):
        return '<User %r>' % self.email_address


class Filters(Document):
    email_address = StringField(null=False, required=True)
    generated = StringField(null=False, primary_key=True, default=address_default)
    enabled = BooleanField(null=False, default=True)
    site = StringField(null=True)

if __name__ == "__main__":
    print(Filters.objects(email_address="kesavarapu.siva@gmail.com"))