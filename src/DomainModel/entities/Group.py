from enum import Enum
from dataclasses import dataclass
from typing import Optional


class GroupMode(Enum):
    wait = 'wait'
    input = 'input'
    tip_input = 'tip_input'
    tip_ok = 'tip_ok'


@dataclass()
class Group:
    id: Optional[int]
    line_group_id: str
    mode: str

    def __init__(
        self,
        line_group_id: str,
        mode: str = GroupMode.wait.value,
        id: Optional[int] = None,
    ):
        self.id = id
        self.line_group_id = line_group_id
        self.mode = mode
