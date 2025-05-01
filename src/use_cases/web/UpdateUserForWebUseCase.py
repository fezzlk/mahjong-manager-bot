from flask import request

from DomainModel.entities.User import User, UserMode
from repositories import session_scope, user_repository


class UpdateUserForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = User(
            line_user_name=form["line_user_name"],
            line_user_id=form["line_user_id"],
            mode=UserMode[form["mode"].split(".")[-1]].value,
            jantama_name=form["jantama_name"],
            _id=int(form["_id"]),
        )
        with session_scope() as session:
            return user_repository.update(session, updated)
