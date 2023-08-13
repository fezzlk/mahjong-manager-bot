from .interfaces.IGroupService import IGroupService
from DomainModel.entities.Group import Group, GroupMode
from repositories import group_repository
from typing import Optional

class GroupService(IGroupService):

    def find_or_create(self, line_group_id: str) -> Group:
        groups = group_repository.find({'line_group_id': line_group_id})

        if len(groups) > 0:
            return groups[0]
    
        group = Group(
            line_group_id=line_group_id,
            mode=GroupMode.wait.value,
        )
        result = group_repository.create(group)
        print(f'create group: ID = {result._id}(line group id: {line_group_id})')
        return result

    def chmod(
        self,
        line_group_id: str,
        mode: GroupMode,
    ) -> None:
        if not isinstance(mode, GroupMode):
            raise ValueError(f'予期しないモード変更リクエストを受け取りました。\'{mode}\'')

        if line_group_id is None:
            raise ValueError('LINE Group ID が None のためモードの変更ができません。')

        result = group_repository.update(
            {'line_group_id': line_group_id},
            {'mode': mode.value},
        )
        if result > 0:
            print(f'chmod: {line_group_id}: {mode.value}')

    def get_mode(self, line_group_id: str) -> GroupMode:
        groups = group_repository.find({'line_group_id': line_group_id})

        if len(groups) == 0:
            return None

        return groups[0].mode

    def find_one_by_line_group_id(self, line_group_id: str) -> Optional[Group]:
        groups = group_repository.find({'line_group_id': line_group_id})

        if len(groups) == 0:
            return None

        return groups[0]

    def update(self, target: Group) -> None:
        group_repository.update(
            {'_id': target._id},
            target.__dict__,
        )