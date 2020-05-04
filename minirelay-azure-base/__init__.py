import logging
from enum import auto, Enum
from .minirelay import *
import azure.functions as func


class Action(Enum):
    REGISTER = "register"
    GENERATE = "generate"
    ENABLE = "enable"
    DISABLE = "disable"
    INBOUND = "inbound"


class ReqParams(object):
    def __init__(self, req: func.HttpRequest):
        self.action = Action[req.params.get('action').upper()]
        self.email = req.params.get("email")  # register/disable
        self.info = req.params.get("info")  # register
        self.enable = req.params.get("enable")
        self.request = req
        if self.enable is not None:
            self.enable = self.enable.lower()
            if self.enable == "false":
                self.enable = False
            elif self.enable == "true":
                self.enable = True
            else:
                self.enable = None


def register(req: ReqParams):
    registerEmail(req.email)


def generate(req):
    return generateEmail(req.email, req.info)


def enable(req):
    enableEmail(req.email, True)


def disable(req):
    enableEmail(req.email, False)


def inbound(req):
    pass
    # inbound_message(req)


def handle_exception_or_code(e: Exception):
    if not e:
        return 200, "Ok"
    if isinstance(e, SpamReducerException):
        return e.code, e.message
    else:
        return SpamReducerException.code, SpamReducerException.code


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req = ReqParams(req)
    action = req.action
    try:
        if action == Action.REGISTER:
            register(req)
        elif action == Action.GENERATE:
            return func.HttpResponse({"success": "ok", "generated": generate(req)}, status_code=200)
        elif action == Action.ENABLE:
            enable(req)
        elif action == Action.DISABLE:
            disable(req)
        elif action == Action.INBOUND:
            inbound(req)
        return func.HttpResponse({"success": "ok"}, status_code=200)
    except Exception as err:
        code, message = handle_exception_or_code(err)
        return func.HttpResponse({"message": message, "success": False, "error": str(err)}, status_code=code)

    if not action:
        return func.HttpResponse(
            "please pass action",
            status_code=400
        )
