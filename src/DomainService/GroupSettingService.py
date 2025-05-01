from DomainModel.entities.GroupSetting import GroupSetting
from repositories import group_setting_repository

from .interfaces.IGroupSettingService import IGroupSettingService


class GroupSettingService(IGroupSettingService):

    def find_or_create(self, line_group_id: str) -> GroupSetting:
        settings = group_setting_repository.find({"line_group_id": line_group_id})

        if len(settings) > 0:
            return settings[0]

        new_settings = GroupSetting(line_group_id=line_group_id)
        result = group_setting_repository.create(new_settings)
        print(f"create group setting: ID = {result._id}(line group id: {line_group_id})")
        return result
