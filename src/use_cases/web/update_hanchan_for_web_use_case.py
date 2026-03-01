from flask import request

from repositories import hanchan_repository

from .web_utils import parse_json_dict, to_object_id, without_id


class UpdateHanchanForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = {
            "_id": to_object_id(form.get("_id")),
            "line_group_id": form.get("line_group_id"),
            "raw_scores": parse_json_dict(form.get("raw_scores"), default={}),
            "converted_scores": parse_json_dict(form.get("converted_scores"), default={}),
            "match_id": to_object_id(form.get("match_id")),
            "status": int(form.get("status")) if form.get("status") is not None else None,
        }
        new_values = {k: v for k, v in without_id(updated).items() if v is not None}
        hanchan_repository.update({"_id": updated["_id"]}, new_values)
