from DomainService import (
    config_service,
)
from ApplicationService import (
    reply_service,
    request_info_service,
)


class ReplyGroupSettingsMenuUseCase:

    def execute(self, body) -> None:
        # リクエスト元ルームIDの取得（ルームからのリクエストでなければユーザーID)
        if request_info_service.req_line_group_id is not None:
            target_id = request_info_service.req_line_group_id
        else:
            target_id = request_info_service.req_line_user_id

        configs = config_service.get_current_settings_by_target(target_id)

        if body == '':
            s = [f'{key}: {str(value)}' for key, value in configs.items()]
            reply_service.add_message('[設定]\n' + '\n'.join(s))

        reply_service.add_settings_menu(body)
