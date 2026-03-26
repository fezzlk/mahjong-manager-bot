from flask import request

from repositories import match_repository

from .web_utils import to_object_id, without_id


class UpdateMatchForWebUseCase:

    def execute(self) -> None:
        form = request.form
        is_deleted_str = form.get("is_deleted")
        updated = {
            "_id": to_object_id(form.get("_id")),
            "line_group_id": form.get("line_group_id"),
            "is_deleted": is_deleted_str.lower() in ("true", "1") if is_deleted_str is not None else None,
        }
        new_values = {k: v for k, v in without_id(updated).items() if v is not None}
        match_repository.update({"_id": updated["_id"]}, new_values)
