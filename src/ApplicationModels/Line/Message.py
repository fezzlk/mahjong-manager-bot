from dataclasses import dataclass
from typing import Dict


@dataclass()
class Message:
    id: str
    text: str
    contentProvider: Dict[str, str]
    message_type: str
    message_type_list = ['text', 'image']  # TODO 要調査

    def __init__(self, text='', message_type='text', id='dummy_message_id'):
        if message_type in self.message_type_list:
            self.type = message_type
        else:
            raise ValueError(
                f'{message_type} is invalid as "message_type" of Message')

        self.id = id

        if message_type == 'image':
            self.contentProvider = {'type': 'line'}
        elif message_type == 'text':
            self.text = text
