from email import message_from_string
from email.utils import parseaddr

import sendgrid
from sendgrid.helpers.mail import Email, Mail
from .models import Filters
from .exceptions import SendGridExceptionMini
from .operations import get_original_email
from .settings import SENDGRID_API_KEY

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)


def inbound(message: str):
    body, sender_email_address, subject, to_email = parse_email(message)
    filter: Filters = get_original_email(to_email)
    from_email_with_name: Email = Email(to_email, f"{filter.info} from {sender_email_address} via minirelay")
    mail = Mail(from_email=from_email_with_name, to_emails=filter.email_adto_email_original_addressdress, subject=subject)
    for part in body:
        mail.add_content(part.get_payload(), part.get_content_type())
    try:
        sg.client.mail.send.post(request_body=mail.get())
    except:
        raise SendGridExceptionMini("exception while submitting to sendgrid")


def parse_email(message):
    parsed_email = message_from_string(message)
    body: str = parsed_email.get_payload()
    _display_name, from_email = parseaddr(parsed_email.get("from"))
    _display_name, to_email = parseaddr(parsed_email.get("to"))
    subject: str = parsed_email.get("subject")
    return body, from_email, subject, to_email
