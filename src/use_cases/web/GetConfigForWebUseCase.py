from repositories import (
    group_setting_repository, session_scope
)
from DomainModel.entities.GroupSetting import Config


class GetConfigForWebUseCase:

    def execute(self, id) -> Config:
        with session_scope() as session:
            records = group_setting_repository.find(session, [_id])
            if len(records) > 0:
                return records[0]
            else:
                None
