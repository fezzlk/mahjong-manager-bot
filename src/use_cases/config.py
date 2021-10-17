"""config"""

from services import (
    request_info_service,
    reply_service,
    config_service,
)

DEFAULT_CONFIGS = {'レート': '点3', '順位点': ','.join(['20', '10', '-10', '-20']),
                   '飛び賞': '10', 'チップ': 'なし', '人数': '4',
                   '端数計算方法': '3万点以下切り上げ/以上切り捨て'}


class ConfigUseCases:
    """config use cases"""

    def update(self, key, value):
        """
        リクエスト元のルームの設定更新
        """
        target_id = request_info_service.req_line_room_id
        config_service.update(target_id, key, value)
        reply_service.add_message(f'{key}を{value}に変更しました。')

    def get(self, ids):
        config_service.get(ids)

    def delete(self, ids):
        config_service.delete(ids)

    def reply_menu(self, body):
        # リクエスト元ルームIDの取得（ルームからのリクエストでなければユーザーID)
        if request_info_service.req_line_room_id is not None:
            target_id = request_info_service.req_line_room_id
        else:
            target_id = request_info_service.req_line_user_id

        configs = config_service.get_by_target(target_id)

        # 返信メッセージ用に変換&返信
        s = [f'{key}: {str(value)}' for key, value in configs.items()]
        reply_service.add_message('[設定]\n' + '\n'.join(s))

        reply_service.add_settings_menu(body)
