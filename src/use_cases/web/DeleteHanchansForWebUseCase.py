from typing import List

from DomainService import (
    match_service,
)
from repositories import hanchan_repository, session_scope


class DeleteHanchansForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        with session_scope() as session:
            deleted_hanchans = hanchan_repository.delete_by_ids(session, ids)
            for deleted_hanchan in deleted_hanchans:
                match_service.remove_hanchan_id(
                    deleted_hanchan.match_id, deleted_hanchan._id,
                )
