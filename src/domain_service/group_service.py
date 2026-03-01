import logging
from typing import Optional, Union

from domain_model.entities.group import Group, GroupMode
from repositories import group_repository

from .interfaces.i_group_service import IGroupService

logger = logging.getLogger(__name__)


class GroupService(IGroupService):

    def find_or_create(self, line_group_id: str) -> Group:
        group = Group(
            line_group_id=line_group_id,
            mode=GroupMode.wait.value,
        )
        return group_repository.find_or_create(group)

    def chmod(
        self,
        line_group_id: str,
        mode: GroupMode,
    ) -> None:
        if not isinstance(mode, GroupMode):
            raise ValueError(f"予期しないモード変更リクエストを受け取りました。'{mode}'")

        if line_group_id is None:
            raise ValueError("LINE Group ID が None のためモードの変更ができません。")

        result = group_repository.update(
            {"line_group_id": line_group_id},
            {"mode": mode.value},
        )
        if result > 0:
            logger.info("chmod: %s: %s", line_group_id, mode.value)

    def get_mode(self, line_group_id: str) -> Optional[str]:
        groups = group_repository.find({"line_group_id": line_group_id})

        if len(groups) == 0:
            return None

        return groups[0].mode

    def find_one_by_line_group_id(self, line_group_id: str) -> Optional[Group]:
        groups = group_repository.find({"line_group_id": line_group_id})

        if len(groups) == 0:
            return None

        return groups[0]

    def update(self, target: Group) -> None:
        group_repository.update(
            {"_id": target._id},
            {k: v for k, v in target.__dict__.items() if k != "_id"},
        )

    def delete_by_line_group_id(self, line_group_id: str) -> None:
        group_repository.delete(
            {"line_group_id": line_group_id},
        )
