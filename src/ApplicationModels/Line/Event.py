from dataclasses import dataclass
from .Source import Source
from .Message import Message
from .Postback import Postback


@dataclass()
class Event:
    type: str
    event_list = ['follow', 'unfollow', 'message', 'postback']  # TODO 要調査

    message_type: str
    text: str
    postback_data: str
    mode: str
    reply_token: str
    postback: Postback
    source: Source

    def __init__(
        self,
        type='message',
        source_type='user',
        user_id='',
        group_id='',
        message_type='text',
        text='dummy_text',
        postback_data='dummy_postback_data',
        mode='active',
    ):
        if type in self.event_list:
            self.type = type
        else:
            raise ValueError(
                f'{type} is invalid as "type" of Event')

        self.source = Source(
            user_id=user_id,
            source_type=source_type,
            group_id=group_id)

        self.mode = mode

        if self.type == 'follow':
            self.reply_token = 'dummy_reply_token'
        if self.type == 'message':
            self.reply_token = 'dummy_reply_token'
            self.message = Message(text=text, message_type=message_type)
        if self.type == 'postback':
            self.reply_token = 'dummy_reply_token'
            self.postback == Postback(data=postback_data)
