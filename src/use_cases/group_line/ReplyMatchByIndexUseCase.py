from ApplicationService import (
    request_info_service,
    reply_service,
    message_service,
)
from DomainService import match_service

class ReplyMatchByIndexUseCase:
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

        match = archived_matches[index-1]
        result = message_service.create_show_match_result(match=match)
    
        reply_service.add_message(f'第{index}回\n{match.created_at.strftime("%Y年%m月%d日")}\n{result}')