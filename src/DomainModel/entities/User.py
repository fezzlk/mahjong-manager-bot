from enum import Enum
from dataclasses import dataclass
from typing import Optional


class UserMode(Enum):
    wait = 'wait'


@dataclass()
class User:
    id: Optional[int]
    name: str
    line_user_id: str
    mode: str
    jantama_name: str

    def __init__(
        self,
        line_user_id: str,
        line_user_name: str = None,
        mode: str = UserMode.wait.value,
        jantama_name: str = None,
        id: Optional[int] = None,
    ):
        if mode not in UserMode:
            raise ValueError(f'UserMode の値({mode})が不適切です。')
   
        self.id = id
        self.line_user_name = line_user_name
        self.line_user_id = line_user_id
        self.mode = mode
        self.jantama_name = jantama_name
