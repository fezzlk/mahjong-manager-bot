from repositories import (
    group_repository, session_scope
)
from DomainModel.entities.Group import Group


class GetGroupForWebUseCase:

    def execute(self, id) -> Group:
        with session_scope() as session:
            records = group_repository.find(session, [_id])
            if len(records) > 0:
                return records[0]
            else:
                None
