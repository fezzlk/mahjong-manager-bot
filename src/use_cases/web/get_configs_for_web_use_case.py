from typing import List

from domain_model.entities.group_setting import GroupSetting
from repositories import group_setting_repository


class GetConfigsForWebUseCase:

    def execute(self) -> List[GroupSetting]:
        return group_setting_repository.find()
