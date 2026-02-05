from flask import request

from repositories import group_setting_repository

from .web_utils import parse_int_list, to_object_id


class UpdateConfigForWebUseCase:
    def execute(self) -> None:
        form = request.form
        target_id = to_object_id(form.get("_id"))
        new_values = {}
        if form.get("line_group_id") is not None:
            new_values["line_group_id"] = form.get("line_group_id")
        if form.get("rate") is not None:
            new_values["rate"] = int(form.get("rate"))
        if form.get("ranking_prize") is not None:
            new_values["ranking_prize"] = parse_int_list(form.get("ranking_prize"))
        if form.get("chip_rate") is not None:
            new_values["chip_rate"] = int(form.get("chip_rate"))
        if form.get("tobi_prize") is not None:
            new_values["tobi_prize"] = int(form.get("tobi_prize"))
        if form.get("num_of_players") is not None:
            new_values["num_of_players"] = int(form.get("num_of_players"))
        if form.get("rounding_method") is not None:
            new_values["rounding_method"] = int(form.get("rounding_method"))
        if new_values:
            group_setting_repository.update({"_id": target_id}, new_values)
