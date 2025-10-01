from typing import List

from DomainModel.entities.GroupSetting import Config
from repositories import group_setting_repository, session_scope


class GetConfigsForWebUseCase:

    def execute(self) -> List[Config]:
        with session_scope() as session:
            return group_setting_repository.find(session)
