from flask import request

from domain_model.entities.user import UserMode
from repositories import user_repository

from .web_utils import parse_enum_value, to_object_id, without_id


class UpdateUserForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = {
            "_id": to_object_id(form.get("_id")),
            "line_user_name": form.get("line_user_name"),
            "line_user_id": form.get("line_user_id"),
            "mode": parse_enum_value(form.get("mode"), UserMode),
            "jantama_name": form.get("jantama_name"),
        }
        user_repository.update({"_id": updated["_id"]}, without_id(updated))
