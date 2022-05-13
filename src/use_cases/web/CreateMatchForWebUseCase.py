from flask import request
from repositories import (
    match_repository, session_scope
)
from DomainModel.entities.Match import Match
import json


class CreateMatchForWebUseCase:

    def execute(self) -> None:
        form = request.form
        new_match = Match(
            line_group_id=form['line_group_id'],
            hanchan_ids=json.loads(form['hanchan_ids']),
            status=int(form['status']),
        )
        with session_scope() as session:
            return match_repository.create(session, new_match)
