from typing import List

from domain_model.entities.group_setting import EmbeddedGroupSettings
from repositories import group_repository


class GetConfigsForWebUseCase:

    def execute(self) -> List[EmbeddedGroupSettings]:
        """全グループの設定を返す（embedded settings を使用）"""
        groups = group_repository.find()
        return [g.settings or EmbeddedGroupSettings() for g in groups]
