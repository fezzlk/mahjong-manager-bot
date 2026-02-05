from typing import Optional

from domain_model.entities.group_setting import GroupSetting
from repositories import group_setting_repository

from .web_utils import to_object_id


class GetConfigForWebUseCase:

    def execute(self, _id) -> Optional[GroupSetting]:
        records = group_setting_repository.find({"_id": to_object_id(_id)})
        return records[0] if len(records) > 0 else None
