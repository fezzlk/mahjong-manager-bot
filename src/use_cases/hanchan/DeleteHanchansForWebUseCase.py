from typing import List
from services import (
    hanchan_service,
    match_service,
)


class DeleteHanchansForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        deleted_hanchans = hanchan_service.delete(ids)
        for deleted_hanchan in deleted_hanchans:
            match_service.remove_hanchan_id(
                deleted_hanchan.match_id, deleted_hanchan.id
            )
