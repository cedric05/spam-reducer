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