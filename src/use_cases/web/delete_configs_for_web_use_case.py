from typing import List

from repositories import group_repository


class DeleteConfigsForWebUseCase:

    def execute(self, line_group_ids: List[str]) -> None:
        """指定グループの settings を削除(embedded を None にリセット)"""
        for line_group_id in line_group_ids:
            group_repository.update(
                {"line_group_id": line_group_id},
                {"settings": None},
            )
