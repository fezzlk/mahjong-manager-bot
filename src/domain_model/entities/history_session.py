from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional

from bson import ObjectId


@dataclass
class HistorySession:
    line_group_id: str
    requester_line_id: str
    selected_line_ids: List[str] = field(default_factory=list)
    expires_at: datetime = field(
        default_factory=lambda: datetime.now() + timedelta(minutes=1),
    )
    _id: Optional[ObjectId] = field(default=None)

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at
