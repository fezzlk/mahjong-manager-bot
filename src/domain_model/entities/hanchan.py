from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Dict, List, Optional

from bson.objectid import ObjectId

if TYPE_CHECKING:
    from domain_model.entities.user_hanchan import UserHanchanResult


@dataclass
class Hanchan:
    line_group_id: str
    match_id: int
    is_deleted: bool = False
    raw_scores: Dict[str, int] = field(default_factory=dict)
    converted_scores: Dict[str, int] = field(default_factory=dict)
    results: List["UserHanchanResult"] = field(default_factory=list)
    original_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    _id: ObjectId = field(default=None)

    def __post_init__(self):  # noqa: D105
        if self.raw_scores is None:
            self.raw_scores = {}
        if self.converted_scores is None:
            self.converted_scores = {}
        if self.results is None:
            self.results = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
