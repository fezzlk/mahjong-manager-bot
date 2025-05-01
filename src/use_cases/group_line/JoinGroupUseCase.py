from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainService import (
    group_service,
)


class JoinGroupUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        if line_group_id is None:
            raise ValueError("登録する line_group_id が未指定です。")
        group_service.find_or_create(line_group_id)
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
