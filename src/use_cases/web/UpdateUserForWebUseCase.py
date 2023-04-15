from flask import request
from repositories import (
    user_repository, session_scope
)
from DomainModel.entities.User import User, UserMode


class UpdateUserForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = User(
            line_user_name=form['line_user_name'],
            line_user_id=form['line_user_id'],
            zoom_url=form['zoom_url'],
            mode=UserMode[form['mode'].split('.')[-1]].value,
            jantama_name=form['jantama_name'],
            _id=int(form['_id']),
        )
        with session_scope() as session:
            return user_repository.update(session, updated)
