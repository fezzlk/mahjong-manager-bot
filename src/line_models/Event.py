from .Source import Source
from .Message import Message
from .Postback import Postback


class Event:
    def __init__(
        self,
        event_type='message',
        source_type='user',
        user_id='',
        group_id='',
        message_type='text',
        text='dummy_text',
        postback_data='dummy_postback_data',
        mode='active',
    ):
        self.type = event_type
        self.replyToken = 'dummy_reply_token'
        self.source = Source(
            user_id=user_id,
            source_type=source_type,
            group_id=group_id)
        self.mode = mode
        if self.type == 'message':
            self.message = Message(text=text, message_type=message_type)
        if self.type == 'postback':
            self.postback == Postback(data=postback_data)
