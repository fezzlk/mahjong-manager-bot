from flask import request
from repositories import (
    yakuman_user_repository, session_scope
)
from DomainModel.entities.YakumanUser import YakumanUser


class UpdateYakumanUserForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = YakumanUser(
            user_id=form['user_id'],
            hanchan_id=form['hanchan_id'],
            _id=int(form['_id']),
        )
        with session_scope() as session:
            return yakuman_user_repository.update(session, updated)
