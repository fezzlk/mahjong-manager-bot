from typing import Optional

from domain_model.entities.hanchan import Hanchan
from repositories import hanchan_repository

from .web_utils import to_object_id


class GetHanchanForWebUseCase:

    def execute(self, _id) -> Optional[Hanchan]:
        records = hanchan_repository.find({"_id": to_object_id(_id)})
        return records[0] if len(records) > 0 else None
