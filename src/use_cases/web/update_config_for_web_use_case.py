from domain_service import group_service, group_setting_service
from flask import request

from .web_utils import parse_int_list


class UpdateConfigForWebUseCase:
    def execute(self) -> None:
        form = request.form
        line_group_id = form.get("line_group_id")
        if not line_group_id:
            return

        # ranking_prize / starting_points は人数ごとに別カラムで保持しているため、
        # 現在の num_of_players に応じて書き込み先カラムを切り替える
        settings = group_setting_service.find_or_create(line_group_id)
        num_of_players = settings.num_of_players
        ranking_prize_column = "ranking_prize_3" if num_of_players == 3 else "ranking_prize_4"
        starting_points_column = "starting_points_3" if num_of_players == 3 else "starting_points_4"

        field_parsers = {
            "rate": ("rate", int),
            "ranking_prize": (ranking_prize_column, parse_int_list),
            "starting_points": (starting_points_column, int),
            "chip_rate": ("chip_rate", int),
            "tobi_prize": ("tobi_prize", int),
            "num_of_players": ("num_of_players", int),
            "rounding_method": ("rounding_method", int),
        }
        for form_key, (column, parser) in field_parsers.items():
            raw = form.get(form_key)
            if raw is not None:
                group_service.update_settings(line_group_id, column, parser(raw))
