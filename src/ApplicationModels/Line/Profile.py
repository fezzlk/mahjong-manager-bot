from dataclasses import dataclass


@dataclass()
class Profile:
    display_name: str
    user_id: str

    def __init__(
        self,
        display_name='',
        user_id='',
    ):
        self.display_name = display_name
        self.user_id = user_id
