from repositories import (
    user_match_repository, session_scope
)
from DomainModel.entities.UserMatch import UserMatch


class GetUserMatchForWebUseCase:

    def execute(self, _id) -> UserMatch:
        with session_scope() as session:
            records = user_match_repository.find_by_ids(session, [_id])
            if len(records) > 0:
                return records[0]
            else:
                None
