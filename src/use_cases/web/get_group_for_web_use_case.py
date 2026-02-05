from typing import Optional

from domain_model.entities.group import Group
from repositories import group_repository

from .web_utils import to_object_id


class GetGroupForWebUseCase:

    def execute(self, _id) -> Optional[Group]:
        records = group_repository.find({"_id": to_object_id(_id)})
        return records[0] if len(records) > 0 else None
