from repositories import (
    config_repository, session_scope
)
from DomainModel.entities.Config import Config


class GetConfigForWebUseCase:

    def execute(self, _id) -> Config:
        with session_scope() as session:
            records = config_repository.find_by_ids(session, [_id])
            if len(records) > 0:
                return records[0]
            else:
                None
