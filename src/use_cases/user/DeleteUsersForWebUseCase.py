from typing import List
from Repositories import (
    user_repository, session_scope,
)


class DeleteUsersForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        with session_scope() as session:
            user_repository.delete_by_ids(
                session=session,
                ids=ids,
            )
