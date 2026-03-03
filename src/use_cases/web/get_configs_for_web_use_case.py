from typing import List

from domain_model.entities.group_setting import EmbeddedGroupSettings
from repositories import group_repository

_SETTINGS_FIELDS = ("rate", "ranking_prize", "chip_rate", "tobi_prize", "num_of_players", "rounding_method")


class GetConfigsForWebUseCase:

    def execute(self) -> List[dict]:
        """全グループの設定を返す(テンプレートが _id キーを参照できるよう dict で返す)"""
        groups = group_repository.find()
        result = []
        for g in groups:
            s = g.settings or EmbeddedGroupSettings()
            d: dict = {"_id": g.line_group_id, "line_group_id": g.line_group_id}
            d.update({k: getattr(s, k) for k in _SETTINGS_FIELDS})
            result.append(d)
        return result
