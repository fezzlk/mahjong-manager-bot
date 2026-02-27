from typing import Optional

from domain_model.entities.group_setting import GroupSetting
from repositories import group_setting_repository

from .web_utils import find_one_by_id


class GetConfigForWebUseCase:

    def execute(self, _id) -> Optional[GroupSetting]:
        return find_one_by_id(group_setting_repository, _id)
