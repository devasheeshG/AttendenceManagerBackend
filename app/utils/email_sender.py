from azure.communication.email import EmailClient
from app.config import get_settings
settings=get_settings()

def send_email(to_email: str, subject: str, body: str):
    client = EmailClient.from_connection_string(settings.ACS_KEY)

    message = {
        "senderAddress": settings.ACS_EMAIL,
        "recipients": {
            "to": [{"address": to_email}]
        },
        "content": {
            "subject": subject,
            "plainText": body
        }
    }

    poller = client.begin_send(message)
    result = poller.result()

    return result