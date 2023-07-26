from flask import request
from repositories import (
    match_repository, session_scope
)
from DomainModel.entities.Match import Match


class UpdateMatchForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = Match(
            line_group_id=form['line_group_id'],
            status=int(form['status']),
            _id=int(form['_id']),
        )
        with session_scope() as session:
            return match_repository.update(session, updated)
