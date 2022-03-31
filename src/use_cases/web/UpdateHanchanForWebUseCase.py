from flask import request
from repositories import (
    hanchan_repository, session_scope
)
from DomainModel.entities.Hanchan import Hanchan
import json


class UpdateHanchanForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = Hanchan(
            line_group_id=form['line_group_id'],
            raw_scores=json.loads(
                form['raw_scores'].replace(
                    "'", '"')),
            converted_scores=json.loads(
                form['converted_scores'].replace(
                    "'", '"')),
            match_id=int(
                form['match_id']),
            status=int(
                form['status']),
            _id=int(
                form['_id']),
        )
        with session_scope() as session:
            return hanchan_repository.update(session, updated)
