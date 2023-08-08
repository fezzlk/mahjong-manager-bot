from DomainService import (
    group_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)


class JoinGroupUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        if line_group_id is None:
            raise ValueError('登録する line_group_id が未指定です。')
        group_service.find_or_create(line_group_id)
        reply_service.add_message(
            '麻雀の成績管理Botです。参加者は友達登録してください。'
        )
        reply_service.add_message(
            '「_start」でスタートメニューを表示します。'
        )
