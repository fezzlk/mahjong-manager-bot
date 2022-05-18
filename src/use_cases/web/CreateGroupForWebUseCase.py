from flask import request
from repositories import (
    group_repository, session_scope
)
from DomainModel.entities.Group import Group, GroupMode


class CreateGroupForWebUseCase:

    def execute(self) -> None:
        form = request.form
        new_group = Group(
            line_group_id=form['line_user_name'],
            zoom_url=form['line_user_name'],
            mode=GroupMode[form['mode'].split('.')[-1]],
            _id=int(form['line_user_name']),
        )
        with session_scope() as session:
            return group_repository.create(session, new_group)