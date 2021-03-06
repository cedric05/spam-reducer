__all__ = ["SpamReducerException", "InValidEmail", "NotRegistered", "AlreadyRegistered",
           "SQLException", "EmailNotGenerated", "NoSuchAction", "NoActionDefined", "DisabledEmail"]


class SpamReducerException(Exception):
    message = "unknown error"
    code = 400


class InValidEmail(SpamReducerException):
    message = "invalid email"
    code = 400


class NotRegistered(SpamReducerException):
    message = "emailid not registered"
    code = 404


class AlreadyRegistered(SpamReducerException):
    message = "already registered"
    code = 409


class SQLException(SpamReducerException):
    message = "sql exception"
    code = 425


class EmailNotGenerated(SpamReducerException):
    message = "email not generated"
    code = 404


class SendGridExceptionMini(SpamReducerException):
    message = "sendgrid provider is running into exception"
    code = 425

class NoSuchAction(SpamReducerException):
    message = "sendgrid provider is running into exception"
    code = 400

class NoActionDefined(SpamReducerException):
    messsage = "No Action defined"
    code = 400

class DisabledEmail(SpamReducerException):
    message = "email disabled"
    code=200