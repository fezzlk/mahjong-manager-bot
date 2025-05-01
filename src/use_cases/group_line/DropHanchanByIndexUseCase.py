from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainService import (
    group_service,
    hanchan_service,
    match_service,
)


class DropHanchanByIndexUseCase:
    def execute(self, str_index: str) -> None:
        if not str_index.isdigit():
            reply_service.add_message(
                "引数は整数で指定してください。",
            )
            return
        index = int(str_index)

        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "トークルームが登録されていません。招待し直してください。",
            )
            return
        if group.active_match_id is None:
            reply_service.add_message(
                "現在進行中の対戦がありません。",
            )
            return

        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match is None:
            raise BaseException(
                f"DropHanchanByIndexUseCase: 対戦結果の取得失敗: match_id: {group.active_match_id}",
            )

        archived_hanchans = hanchan_service.find_all_archived_by_match_id(
            match_id=active_match._id,
        )

        if index < 1 or len(archived_hanchans) < index:
            reply_service.add_message(
                f"このトークルームには全{len(archived_hanchans)}回までしか登録されていないため第{index}回はありません。",
            )
            return

        target_hanchan = archived_hanchans[index - 1]
        target_hanchan.status = 0
        hanchan_service.update(target_hanchan)
        reply_service.add_message(
            f"現在の対戦の第{index}半荘の結果を削除しました。",
        )
