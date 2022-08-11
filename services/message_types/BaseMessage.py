
from main.models import Messages


class BaseMessage:
    def execute(self, message_object) -> str:
        return "{} Default Message".format(message_object.message_from)


class MessageTypeContext:
    def __init__(self, default_strategy) -> None:
        self.strategy = default_strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, message_object: Messages):
        self.strategy.execute(message_object)
