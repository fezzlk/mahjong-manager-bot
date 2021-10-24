from typing import List
from .interfaces.IRoomService import IRoomService
from domains.Room import Room, RoomMode
from repositories import session_scope, room_repository


class RoomService(IRoomService):

    def find_or_create(self, room_id: str) -> Room:
        with session_scope() as session:
            room = room_repository.find_one_by_room_id(session, room_id)

            if room is None:
                room = Room(
                    line_room_id=room_id,
                    zoom_url=None,
                    mode=RoomMode.wait,
                )
                room_repository.create(session, room)
                print(f'create room: {room_id}')

            return room

    def chmod(
        self,
        line_room_id: str,
        mode: RoomMode,
    ) -> Room:
        if mode not in RoomMode:
            print(
                'failed to change mode: unexpected mode request received.'
            )
            return None

        with session_scope() as session:
            record = room_repository.update_one_mode_by_line_room_id(
                session,
                line_room_id,
                mode
            )
            if record is None:
                print(
                    'failed to change mode: room is not found'
                )
                return None

            return record

    def get_mode(self, line_room_id: str) -> RoomMode:
        with session_scope() as session:
            # find にし、複数件ヒットした場合にはエラーを返す
            target = room_repository.find_one_by_room_id(session, line_room_id)

            if target is None:
                print(
                    'failed to get mode: room is not found'
                )
                raise Exception('トークルームが登録されていません。招待し直してください。')

            return target.mode

    def get(self, ids: List[int] = None) -> List[Room]:
        with session_scope() as session:
            if ids is None:
                return room_repository.find_all(session)

            return room_repository.find_by_ids(session, ids)

    def delete(self, ids: List[int]) -> None:
        with session_scope() as session:
            room_repository.delete_by_ids(session, ids)

        print(f'delete: id={ids}')

    def set_zoom_url(
        self,
        line_room_id: str,
        zoom_url: str,
    ) -> Room:
        with session_scope() as session:
            record = room_repository.update_one_zoom_url_by_line_room_id(
                session,
                line_room_id,
                zoom_url,
            )

            if record is None:
                print(
                    f'fail to set zoom url: room "{line_room_id}" is not found')
                raise Exception('トークルームが登録されていません。招待し直してください。')

            print(f'set_zoom_url: {zoom_url} to {line_room_id}')
            return record

    def get_zoom_url(
        self,
        line_room_id: str,
    ) -> str:
        with session_scope() as session:
            target = room_repository.find_one_by_room_id(session, line_room_id)

            if target is None:
                print(
                    f'fail to get zoom url: room "{line_room_id}" is not found.')
                raise Exception('トークルームが登録されていません。招待し直してください。')

            if target.zoom_url is None:
                print(
                    f'fail to get zoom url: room "{line_room_id}" does not have zoom url.')
                return None

            return target.zoom_url
