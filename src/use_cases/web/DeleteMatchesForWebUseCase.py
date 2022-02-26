from typing import List
from DomainService import (
    match_service,
    hanchan_service,
)


class DeleteMatchesForWebUseCase:

    def execute(self, target_ids: List[int]) -> None:
        targets = match_service.delete(target_ids)
        for target in targets:
            hanchan_service.delete(target.hanchan_ids)
        print(f'delete match: id={target_ids}')
