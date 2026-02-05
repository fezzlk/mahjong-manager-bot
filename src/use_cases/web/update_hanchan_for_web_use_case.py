import json
from flask import request

from repositories import hanchan_repository

from .web_utils import to_object_id, without_id


class UpdateHanchanForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = {
            "_id": to_object_id(form.get("_id")),
            "line_group_id": form.get("line_group_id"),
            "raw_scores": json.loads(form.get("raw_scores", "{}").replace("'", '"')),
            "converted_scores": json.loads(form.get("converted_scores", "{}").replace("'", '"')),
            "match_id": to_object_id(form.get("match_id")),
            "status": int(form.get("status")) if form.get("status") is not None else None,
        }
        hanchan_repository.update({"_id": updated["_id"]}, without_id(updated))
