import json

from flask import request

from DomainModel.entities.Hanchan import Hanchan
from repositories import hanchan_repository, session_scope


class UpdateHanchanForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = Hanchan(
            line_group_id=form["line_group_id"],
            raw_scores=json.loads(
                form["raw_scores"].replace(
                    "'", '"')),
            converted_scores=json.loads(
                form["converted_scores"].replace(
                    "'", '"')),
            match_id=int(
                form["match_id"]),
            status=int(
                form["status"]),
            _id=int(
                form["_id"]),
        )
        with session_scope() as session:
            return hanchan_repository.update(session, updated)
