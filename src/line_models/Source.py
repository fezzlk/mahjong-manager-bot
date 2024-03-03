class Source:
    def __init__(
        self,
        user_id='',
        source_type='user',
        group_id='',
    ):
        self.type = source_type
        self.user_id = user_id

        if source_type == 'group':
            self.group_id = group_id
        if source_type == 'room':
            self.room_id = group_id
