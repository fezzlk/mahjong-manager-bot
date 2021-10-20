from typing import List
from services import (
    match_service,
    hanchan_service,
)
import json
from server import logger


class DeleteMatchesForWebUseCase:

    def execute(self, target_ids: List[int]) -> None:
        targets = match_service.delete(target_ids)
        for target in targets:
            hanchan_service.delete(
                json.loads(target.result_ids)
            )
        logger.info(f'delete match: id={target_ids}')
