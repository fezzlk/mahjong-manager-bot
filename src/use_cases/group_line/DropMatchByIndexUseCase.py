from DomainService import (
    match_service,
    hanchan_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)


class DropMatchByIndexUseCase:

    def execute(self, str_index: str) -> None:
        line_group_id = request_info_service.req_line_group_id
        archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
        if not str_index.isdigit():
            reply_service.add_message(
                '引数は整数で指定してください。'
            )
            return

        index = int(str_index)
        if index < 1 or len(archived_matches) < index:
            reply_service.add_message(
                f'このトークルームには全{len(archived_matches)}回までしか登録されていないため第{index}回はありません。'
            )
            return

        target_match = archived_matches[index-1]
        hanchan_service.disable_by_match_id(match_id=target_match._id)
        target_match.status = 0
        match_service.update(target_match)
        reply_service.add_message(
            f'第{index}回の対戦結果を削除しました。'
        )