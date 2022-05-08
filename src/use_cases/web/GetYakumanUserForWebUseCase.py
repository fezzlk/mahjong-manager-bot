from repositories import (
    yakuman_user_repository, session_scope
)
from DomainModel.entities.YakumanUser import YakumanUser


class GetYakumanUserForWebUseCase:

    def execute(self, _id) -> YakumanUser:
        with session_scope() as session:
            records = yakuman_user_repository.find_by_ids(session, [_id])
            if len(records) > 0:
                return records[0]
            else:
                None
