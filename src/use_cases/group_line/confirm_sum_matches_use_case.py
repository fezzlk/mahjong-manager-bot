from bson.errors import InvalidId
from bson.objectid import ObjectId

from application_service import reply_service, request_info_service
from domain_service import match_service, user_service
from repositories import match_sum_session_repository

_TIMEOUT_MSG = "タイムアウトしました。その他メニューの「まとめて精算」から再度お試しください。"


class ConfirmSumMatchesUseCase:
    def execute(self) -> None:
        """_sum_matches_confirm: 選択された対戦の合計を表示する。"""
        line_group_id = request_info_service.req_line_group_id

        session = match_sum_session_repository.find_active_by_group_id(line_group_id)
        if session is None:
            reply_service.add_message(_TIMEOUT_MSG)
            return

        if not session.selected_match_ids:
            archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
            recent = archived_matches[-10:]
            start_index = len(archived_matches) - len(recent) + 1
            reply_service.add_message("対戦を選んでください。")
            reply_service.add_sum_matches_select_quick_reply(recent, start_index, [])
            return

        match_object_ids = [
            oid for oid in (_to_object_id(mid) for mid in session.selected_match_ids) if oid is not None
        ]

        matches = match_service.find_all_by_ids_and_line_group_ids(
            ids=match_object_ids,
            line_group_ids=[line_group_id],
        )

        total: dict = {}
        for match in matches:
            prices = match.sum_prices_with_chip or match.sum_prices
            for line_user_id, price in prices.items():
                total[line_user_id] = total.get(line_user_id, 0) + price

        match_sum_session_repository.delete_by_group_id(line_group_id)

        if not total:
            reply_service.add_message("選択した対戦に精算結果がありません。")
            return

        lines = [f"選択した{len(matches)}件の対戦の合計:"]
        for line_user_id, price in total.items():
            name = user_service.get_name_by_line_user_id(line_user_id) or "友達未登録"
            str_price = ("+" + str(price)) if price > 0 else str(price)
            lines.append(f"{name}: {str_price}円")
        reply_service.add_message("\n".join(lines))


def _to_object_id(match_id: str):
    try:
        return ObjectId(match_id)
    except InvalidId:
        return None
