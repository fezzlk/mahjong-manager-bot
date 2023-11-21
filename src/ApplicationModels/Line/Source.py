from dataclasses import dataclass


@ dataclass
class Source:
    type: str
    source_type_list = ['user', 'group', 'room']
    user_id: str
    group_id: str

    def __init__(
        self,
        user_id='',
        source_type='user',
        group_id='',
    ):
        if source_type in self.source_type_list:
            self.type = source_type
        else:
            raise ValueError(
                f'{source_type} is invalid as "source_type" of Source')

        self.user_id = user_id

        if source_type == 'group':
            self.group_id = group_id
