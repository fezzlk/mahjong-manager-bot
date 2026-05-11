import logging

from linebot.v3.messaging.exceptions import ApiException

from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import (
    group_service,
)
from messaging_api_setting import line_bot_api

logger = logging.getLogger(__name__)


class JoinGroupUseCase:
    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        if line_group_id is None:
            raise ValueError("登録する line_group_id が未指定です。")
        logger.info("join group: group=%s", line_group_id)
        group_service.find_or_create(line_group_id)
        try:
            summary = line_bot_api.get_group_summary(line_group_id)
            group_service.update_group_info(
                line_group_id,
                summary.group_name,
                summary.picture_url,
            )
        except ApiException:
            logger.warning("get_group_summary failed: group=%s", line_group_id)
        reply_service.add_message(
            "麻雀の成績管理Botです。参加者は友達登録してください。",
        )
        reply_service.add_message(
            "1半荘が終了したら下のメニューの「結果を入力」を押し、それぞれ素点を入力して下さい。",
        )
        reply_service.add_message(
            "レートや点数計算方法は「設定」で変更可能です。",
        )
        reply_service.add_start_menu()
