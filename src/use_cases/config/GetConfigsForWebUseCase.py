from typing import List
from repositories import (
    config_repository, session_scope
)
from Entities.Config import Config


class GetConfigsForWebUseCase:

    def execute(self) -> List[Config]:
        with session_scope() as session:
            return config_repository.find_all(session)
