from typing import List

from repositories import group_repository, session_scope


class DeleteGroupsForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        with session_scope() as session:
            group_repository.delete_by_ids(session, ids)
