class Message:
    def __init__(self, text='', message_type='text'):
        self.type = message_type
        self._id = 'dummy_message_id'

        if message_type == 'image':
            self.contentProvider = {'type': 'line'}
        elif message_type == 'text':
            self.text = text
