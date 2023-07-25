from enum import Enum
from dataclasses import dataclass
from bson.objectid import ObjectId


class GroupMode(Enum):
    wait = 'wait'
    input = 'input'
    tip_input = 'tip_input'
    tip_ok = 'tip_ok'


@dataclass()
class Group:
    _id: ObjectId
    line_group_id: str
    mode: str

    def __init__(
        self,
        line_group_id: str,
        mode: str = GroupMode.wait.value,
        _id: ObjectId = None,
    ):
        if mode not in GroupMode._member_names_:
            raise ValueError(f'GroupMode の値({mode})が不適切です。')
   
        self._id = _id
        self.line_group_id = line_group_id
        self.mode = mode
