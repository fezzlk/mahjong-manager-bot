from typing import List
from services import (
    config_service,
)
from domains.Config import Config


class GetConfigsForWebUseCase:

    def execute(self) -> List[Config]:
        config_service.get()
