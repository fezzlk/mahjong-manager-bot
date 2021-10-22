from typing import List
from services import (
    config_service,
)
from domains.Config import Config


class GetConfigsForWebUseCase:

    def execute(self) -> List[Config]:
        return config_service.get()
