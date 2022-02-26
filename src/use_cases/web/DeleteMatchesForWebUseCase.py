from typing import List
from repositories import session_scope, match_repository


class DeleteMatchesForWebUseCase:

    def execute(self, target_ids: List[int]) -> None:
        with session_scope() as session:
            match_repository.delete_by_ids(session, target_ids)
