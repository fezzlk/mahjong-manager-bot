from typing import List
from repositories import (
    group_setting_repository, session_scope
)
from DomainModel.entities.GroupSetting import Config


class GetConfigsForWebUseCase:

    def execute(self) -> List[Config]:
        with session_scope() as session:
            return group_setting_repository.find(session)
