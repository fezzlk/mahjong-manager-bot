# flake8: noqa: E999
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    id: int
    target_id: str
    key: str
    value: str
