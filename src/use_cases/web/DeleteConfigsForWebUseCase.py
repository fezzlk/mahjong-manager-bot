from typing import List

from repositories import group_setting_repository, session_scope


class DeleteConfigsForWebUseCase:

    def execute(self, ids: List[int]):
        with session_scope() as session:
            group_setting_repository.delete_by_ids(
                session=session,
                ids=ids,
            )
