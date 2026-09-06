from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import guest_service


class GuestAddUseCase:
    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        guest = guest_service.register_next(line_group_id)
        reply_service.add_message(f"「ゲスト{guest.guest_number}」を追加しました。")
