from .Mention import Mention


class Message:
    def __init__(
        self,
        text="",
        message_type="text",
        mention_ids=None,
    ):
        self.type = message_type
        self._id = "dummy_message_id"
        self.mention = Mention(mention_ids=mention_ids)

        if message_type == "image":
            self.contentProvider = {"type": "line"}
        elif message_type == "text":
            self.text = text
