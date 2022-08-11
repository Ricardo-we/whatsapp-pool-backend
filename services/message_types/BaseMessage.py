
class BaseMessage:
    def execute(self, message_object) -> str:
        return "{} Default Message".format(message_object.message_from)
