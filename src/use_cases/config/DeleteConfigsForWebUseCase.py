from typing import List
from services import (
    config_service,
)


class DeleteConfigsForWebUseCase:

    def execute(self, ids: List[int]):
        config_service.delete(ids)
