from typing import List
from services import (
    match_service,
    hanchan_service,
)
from server import logger


class DeleteMatchesForWebUseCase:

    def execute(self, target_ids: List[int]) -> None:
        targets = match_service.delete(target_ids)
        for target in targets:
            hanchan_service.delete(target.hanchan_ids)
        logger.info(f'delete match: id={target_ids}')
