from typing import List
from Repositories import config_repository, session_scope


class DeleteConfigsForWebUseCase:

    def execute(self, ids: List[int]):
        with session_scope() as session:
            config_repository.delete_by_ids(
                session=session,
                ids=ids
            )
