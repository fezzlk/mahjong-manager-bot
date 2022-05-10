from typing import List
from repositories import (
    yakuman_user_repository, session_scope,
)


class DeleteYakumanUsersForWebUseCase:

    def execute(self, ids: List[int]) -> None:
        with session_scope() as session:
            yakuman_user_repository.delete_by_ids(
                session=session,
                ids=ids,
            )
