from flask import request

from DomainModel.entities.Match import Match
from repositories import match_repository, session_scope


class UpdateMatchForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = Match(
            line_group_id=form["line_group_id"],
            status=int(form["status"]),
            _id=int(form["_id"]),
        )
        with session_scope() as session:
            return match_repository.update(session, updated)
