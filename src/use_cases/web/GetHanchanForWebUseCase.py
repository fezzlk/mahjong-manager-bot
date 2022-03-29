from DomainModel.entities.Hanchan import Hanchan
from repositories import session_scope, hanchan_repository


class GetHanchanForWebUseCase:

    def execute(self, _id) -> Hanchan:
        with session_scope() as session:
            records = hanchan_repository.find_by_ids(session, [_id])
            if len(records) > 0:
                return records[0]
            else:
                None
