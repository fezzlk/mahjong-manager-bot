from flask import request
from repositories import (
    config_repository, session_scope
)
from DomainModel.entities.Config import Config


class UpdateConfigForWebUseCase:

    def execute(self) -> None:
        form = request.form
        updated = Config(
            target_id=form['target_id'],
            key=form['key'],
            value=form['value'],
            _id=int(form['_id']),
        ),
        with session_scope() as session:
            return config_repository.update(session, updated)
