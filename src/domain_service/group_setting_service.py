from domain_model.entities.group_setting import GroupSetting
from repositories import group_setting_repository

from .interfaces.i_group_setting_service import IGroupSettingService


class GroupSettingService(IGroupSettingService):

    def find_or_create(self, line_group_id: str) -> GroupSetting:
        new_settings = GroupSetting(line_group_id=line_group_id)
        return group_setting_repository.find_or_create(new_settings)
