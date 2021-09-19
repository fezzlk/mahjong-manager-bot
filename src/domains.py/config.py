# flake8: noqa: E999
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    id: int
    target_id: str
    key: str
    value: str

# TODO: 値オブジェクト化
# target_id は LINE の　ユーザーID or Room ID 
# 接頭辞は U or R

# key は Enum

# value は Enum