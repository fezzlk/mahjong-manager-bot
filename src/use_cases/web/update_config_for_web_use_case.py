from flask import request

from domain_service import group_service

from .web_utils import parse_int_list


class UpdateConfigForWebUseCase:
    def execute(self) -> None:
        form = request.form
        line_group_id = form.get("line_group_id")
        if not line_group_id:
            return

        field_parsers = {
            "rate": int,
            "ranking_prize": parse_int_list,
            "chip_rate": int,
            "tobi_prize": int,
            "num_of_players": int,
            "rounding_method": int,
        }
        for column, parser in field_parsers.items():
            raw = form.get(column)
            if raw is not None:
                group_service.update_settings(line_group_id, column, parser(raw))
