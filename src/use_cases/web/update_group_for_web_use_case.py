from flask import request

from domain_model.entities.group import GroupMode
from repositories import group_repository

from .web_utils import parse_enum_value, to_object_id, without_id


class UpdateGroupForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = {
            "_id": to_object_id(form.get("_id")),
            "line_group_id": form.get("line_group_id"),
            "mode": parse_enum_value(form.get("mode"), GroupMode),
            "active_match_id": to_object_id(form.get("active_match_id")),
        }
        new_values = {k: v for k, v in without_id(updated).items() if v is not None}
        group_repository.update({"_id": updated["_id"]}, new_values)
