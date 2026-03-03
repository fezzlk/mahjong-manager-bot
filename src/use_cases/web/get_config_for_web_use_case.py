from typing import Optional

from domain_model.entities.group_setting import EmbeddedGroupSettings
from repositories import group_repository

from .web_utils import to_object_id


class GetConfigForWebUseCase:

    def execute(self, line_group_id: str) -> Optional[EmbeddedGroupSettings]:
        groups = group_repository.find({"line_group_id": line_group_id})
        if not groups:
            return None
        return groups[0].settings or EmbeddedGroupSettings()
