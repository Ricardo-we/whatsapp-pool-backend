from .BaseMessage import BaseMessage
from django.core.mail import send_mail


class WhatsappMessageStrategy(BaseMessage):
    def execute(self, message_object) -> str:
        return send_mail(
            message_object.user.username,
            message_object.message,
            message_object.user.email,
            [message_object.contact_info],
            fail_silently=False,
        )
