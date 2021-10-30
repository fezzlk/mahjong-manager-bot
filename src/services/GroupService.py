from typing import List
from .interfaces.IGroupService import IGroupService
from domains.Group import Group, GroupMode
from repositories import session_scope, group_repository


class GroupService(IGroupService):

    def find_or_create(self, group_id: str) -> Group:
        with session_scope() as session:
            group = group_repository.find_one_by_line_group_id(
                session, group_id)

            if group is None:
                group = Group(
                    line_group_id=group_id,
                    zoom_url=None,
                    mode=GroupMode.wait,
                )
                group_repository.create(session, group)
                print(f'create group: {group_id}')

            return group

    def chmod(
        self,
        line_group_id: str,
        mode: GroupMode,
    ) -> Group:
        if mode not in GroupMode:
            print(
                'failed to change mode: unexpected mode request received.'
            )
            return None

        with session_scope() as session:
            record = group_repository.update_one_mode_by_line_group_id(
                session,
                line_group_id,
                mode
            )
            if record is None:
                print(
                    'failed to change mode: group is not found'
                )
                return None

            return record

    def get_mode(self, line_group_id: str) -> GroupMode:
        with session_scope() as session:
            # find にし、複数件ヒットした場合にはエラーを返す
            target = group_repository.find_one_by_line_group_id(
                session, line_group_id)

            if target is None:
                print(
                    'failed to get mode: group is not found'
                )
                raise Exception('トークルームが登録されていません。招待し直してください。')

            return target.mode

    def get(self, ids: List[int] = None) -> List[Group]:
        with session_scope() as session:
            if ids is None:
                return group_repository.find_all(session)

            return group_repository.find_by_ids(session, ids)

    def delete(self, ids: List[int]) -> None:
        with session_scope() as session:
            group_repository.delete_by_ids(session, ids)

        print(f'delete: id={ids}')

    def set_zoom_url(
        self,
        line_group_id: str,
        zoom_url: str,
    ) -> Group:
        with session_scope() as session:
            record = group_repository.update_one_zoom_url_by_line_group_id(
                session,
                line_group_id,
                zoom_url,
            )

            if record is None:
                print(
                    f'fail to set zoom url: group "{line_group_id}" is not found')
                raise Exception('トークルームが登録されていません。招待し直してください。')

            print(f'set_zoom_url: {zoom_url} to {line_group_id}')
            return record

    def get_zoom_url(
        self,
        line_group_id: str,
    ) -> str:
        with session_scope() as session:
            target = group_repository.find_one_by_line_group_id(
                session, line_group_id)

            if target is None:
                print(
                    f'fail to get zoom url: group "{line_group_id}" is not found.')
                raise Exception('トークルームが登録されていません。招待し直してください。')

            if target.zoom_url is None:
                print(
                    f'fail to get zoom url: group "{line_group_id}" does not have zoom url.')
                return None

            return target.zoom_url
