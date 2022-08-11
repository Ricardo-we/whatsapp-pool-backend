from main.models import Messages
from .EmailStrategy import EmailMessageStrategy
from .WhatsappStrategy import WhatsappMessageStrategy


class MessageTypeContext:
    def __init__(self, default_strategy) -> None:
        self.strategy = default_strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, message_object: Messages):
        self.strategy.execute(message_object)


def execute_method(message_object, type="email"):
    context = MessageTypeContext(EmailMessageStrategy())
    if type == "whatsapp":
        context.set_strategy(WhatsappMessageStrategy())

    context.execute_strategy(message_object)
