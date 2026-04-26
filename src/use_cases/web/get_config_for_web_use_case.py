from typing import Optional

from domain_model.entities.group_setting import EmbeddedGroupSettings
from repositories import group_repository

_SETTINGS_FIELDS = ("rate", "ranking_prize", "chip_rate", "tobi_prize", "num_of_players", "rounding_method")


class GetConfigForWebUseCase:

    def execute(self, line_group_id: str) -> Optional[dict]:
        groups = group_repository.find({"line_group_id": line_group_id})
        if not groups:
            return None
        g = groups[0]
        s = g.settings or EmbeddedGroupSettings()
        d: dict = {"_id": g.line_group_id, "line_group_id": g.line_group_id}
        d.update({k: getattr(s, k) for k in _SETTINGS_FIELDS})
        return d
