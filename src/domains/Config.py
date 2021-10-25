from dataclasses import dataclass


@dataclass()
class Config:
    _id: int
    target_id: str
    key: str
    value: str

    def __init__(
        self,
        target_id: str,
        key: str,
        value: str,
        _id=None,
    ):
        self._id = _id
        self.target_id = target_id
        self.key = key
        self.value = value

# TODO: 値オブジェクト化
# target_id は LINE の　ユーザーID or Group ID or Group ID
# 接頭辞は U or R or G

# key は Enum

# value は Enum
