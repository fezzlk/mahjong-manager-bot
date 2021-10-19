from services import (
    request_info_service,
    config_service,
    reply_service,
)


class UpdateConfigUseCase:

    def execute(self, key: str, value: str):
        """
        リクエスト元のルームの設定更新
        """
        target_id = request_info_service.req_line_room_id
        config_service.update(target_id, key, value)
        reply_service.add_message(f'{key}を{value}に変更しました。')
