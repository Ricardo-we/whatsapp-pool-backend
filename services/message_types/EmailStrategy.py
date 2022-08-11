from xmlrpc.client import boolean
from .BaseMessage import BaseMessage
from django.core.mail import send_mail
from django.conf import settings


class EmailMessageStrategy(BaseMessage):
    def execute(self, message_object) -> bool:
        try:
            print("Sending")
            send_mail(
                message_object.user.username,
                message_object.message,
                settings.EMAIL_HOST_USER,
                [message_object.contact_info],
                fail_silently=False,
            )
            return True
        except Exception as error:
            print(error)
            return False
