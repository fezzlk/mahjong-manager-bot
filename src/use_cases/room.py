"""room"""

from server import logger
from services import (
    reply_service,
    room_service,
    match_service,
    request_info_service,
    hanchan_service,
    user_service,
)


class RoomUseCases:
    """room use cases"""

    def join(self):
        """join event"""
        reply_service.add_message(
            'こんにちは、今日は麻雀日和ですね。'
        )
        room_id = request_info_service.req_line_room_id
        if room_id is None:
            logger.warning('This request is not from room chat')
            return
        room_service.find_or_create(room_id)

    def reply_mode(self):
        room_id = request_info_service.req_line_room_id
        mode = room_service.get_mode(room_id)
        reply_service.add_message(mode)

    def get(self, ids=None):
        room_service.get(ids)

    def delete(self, ids):
        room_service.delete(ids)

    def set_zoom_url(self, zoom_url=None):
        if zoom_url is None:
            user_id = request_info_service.req_line_user_id
            user = user_service.find_by_line_user_id(user_id)

            if user is None:
                logger.warning(
                    f'set_zoom_url: user(id={user_id}) is not found')
                return

            zoom_url = user.zoom_id

        room_id = request_info_service.req_line_room_id
        result_zoom_url = room_service.set_zoom_url(room_id, zoom_url)

        if result_zoom_url is None:
            return

        reply_service.add_message(
            'Zoom URL を登録しました。\n「_zoom」で呼び出すことができます。')

    def reply_zoom_url(self):
        room_id = request_info_service.req_line_room_id
        result_zoom_url = room_service.get_zoom_url(room_id)

        if result_zoom_url is None:
            reply_service.add_message('Zoom URL を取得できませんでした。')
            return

        reply_service.add_message(result_zoom_url)

    def wait_mode(self):
        room_id = request_info_service.req_line_room_id
        hanchan_service.disable(room_id)
        room_service.chmod(
            room_id,
            room_service.modes.wait,
        )
        reply_service.add_message(
            '始める時は「_start」と入力してください。')

    def input_mode(self):
        room_id = request_info_service.req_line_room_id
        updated_mode = room_service.chmod(
            room_id,
            room_service.modes.input,
        )
        reply_service.add_message(
            f'第{match_service.count_results()+1}回戦お疲れ様です。各自点数を入力してください。\
            \n（同点の場合は上家が高くなるように数点追加してください）')
        return
