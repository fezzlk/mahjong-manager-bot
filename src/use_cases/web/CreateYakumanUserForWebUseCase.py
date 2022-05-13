from flask import request
from repositories import (
    yakuman_user_repository, session_scope
)
from DomainModel.entities.YakumanUser import YakumanUser


class CreateYakumanUserForWebUseCase:

    def execute(self) -> None:
        form = request.form
        new_yakuman_user = YakumanUser(
            user_id=form['user_id'],
            hanchan_id=form['hanchan_id'],
        )
        with session_scope() as session:
            return yakuman_user_repository.create(session, new_yakuman_user)
