from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import guest_service


class GuestRemoveConfirmUseCase:
    """_guest_remove_confirm?number=<N>: ゲストの削除を確定する。"""

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        number = request_info_service.params.get("number")

        if not number or not number.isdigit():
            reply_service.add_message("削除するゲストが指定されていません。")
            return

        removed = guest_service.remove(line_group_id, int(number))
        if not removed:
            reply_service.add_message("指定されたゲストが見つかりません。")
            return

        reply_service.add_message(f"「ゲスト{number}」を削除しました。")
