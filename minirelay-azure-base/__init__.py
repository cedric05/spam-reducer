import logging
from enum import auto, Enum
from .minirelay import *
import azure.functions as func
import json


class Action(Enum):
    REGISTER = "register"
    GENERATE = "generate"
    ENABLE = "enable"
    DISABLE = "disable"
    INBOUND = "inbound"
    SETUP = "setup"
    LIST = "list"


class ReqParams(object):
    def __init__(self, req: func.HttpRequest):
        action = req.params.get('action')
        if action != None:
            self.action = Action[action.upper()]
        else:
            self.action = None;
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


def setup_db():
    setup()


def register(req: ReqParams):
    registerEmail(req.email)


def generate(req):
    return generateEmail(req.email, req.info)


def enable(req):
    enableEmail(req.email, True)


def disable(req):
    enableEmail(req.email, False)


def inbound(reqParams: ReqParams):
    request = reqParams.request
    # by default it is paracable 
    email = reqParams.request.form.get("email")
    inbound_message(email)


def handle_exception_or_code(e: Exception):
    if not e:
        return 200, "Ok"
    logging.exception("failed with error")
    if isinstance(e, SpamReducerException):
        return e.code, e.message, e.__class__.__name__
    else:
        return SpamReducerException.code, SpamReducerException.code, "not identified"


class JsonHttpResponse(func.HttpResponse):
    def __init__(self, body={}, status_code=200, headers={}, *args, **kwargs):
        body = json.dumps(body)
        headers["Content-type"] = "application/atom+xml; charset=utf-8"
        super().__init__(body=body, *args, **kwargs)


def list_emails_action(req):
    return listEmail(req.email)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req = ReqParams(req)
    action = req.action
    if action:
        try:
            if action == Action.SETUP:
                setup_db()
            elif action == Action.REGISTER:
                register(req)
            elif action == Action.GENERATE:
                return JsonHttpResponse({"success": "ok", "response": {"generated": generate(req)}}, status_code=200)
            elif action == Action.ENABLE:
                enable(req)
            elif action == Action.DISABLE:
                disable(req)
            elif action == Action.INBOUND:
                inbound(req)
            elif action == Action.LIST:
                return JsonHttpResponse({"success": "ok", "response": list_emails_action(req)}, status_code=200)
            return JsonHttpResponse({"success": "ok"}, status_code=200)
        except Exception as err:
            code, message, error_code = handle_exception_or_code(err)
            return JsonHttpResponse({"message": message, "error_code": error_code, "success": False, "error": str(err)},
                                    status_code=code)

    return JsonHttpResponse(
        {"message": "action not available", "success": False},
        status_code=400
    )
