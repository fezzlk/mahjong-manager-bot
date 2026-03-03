from domain_model.entities.group_setting import EmbeddedGroupSettings

from .interfaces.i_group_setting_service import IGroupSettingService


class GroupSettingService(IGroupSettingService):
    """後方互換のための薄いラッパー。group_service.get_settings_or_create() に委譲する(DB-02 migration 後に削除予定)"""

    def find_or_create(self, line_group_id: str) -> EmbeddedGroupSettings:
        from domain_service.group_service import GroupService  # noqa: PLC0415
        return GroupService().get_settings_or_create(line_group_id)
