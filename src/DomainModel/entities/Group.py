from enum import Enum
from dataclasses import dataclass


class GroupMode(Enum):
    wait = 'wait'
    input = 'input'


@dataclass()
class Group:
    _id: int
    line_group_id: str
    zoom_url: str
    mode: GroupMode

    def __init__(
        self,
        line_group_id: str,
        mode: GroupMode,
        zoom_url: str = None,
        _id=None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.mode = mode
        self.zoom_url = zoom_url
