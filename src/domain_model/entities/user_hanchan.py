from dataclasses import dataclass, field
from datetime import datetime

from bson.objectid import ObjectId


@dataclass
class UserHanchanResult:
    """Hanchan に embedded される結果（_id・hanchan_id なし）"""

    line_user_id: str
    rank: int
    point: int
    yakuman_count: int = 0

    def to_dict(self) -> dict:
        return {
            "line_user_id": self.line_user_id,
            "rank": self.rank,
            "point": self.point,
            "yakuman_count": self.yakuman_count,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "UserHanchanResult":
        return cls(
            line_user_id=d["line_user_id"],
            rank=d["rank"],
            point=d["point"],
            yakuman_count=d.get("yakuman_count", 0),
        )


@dataclass
class UserHanchan:
    line_user_id: str
    hanchan_id: ObjectId
    point: int
    rank: int
    yakuman_count: int = field(default=0)
    _id: ObjectId = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):  # noqa: D105
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
