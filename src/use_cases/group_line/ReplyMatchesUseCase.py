from ApplicationService import (
    request_info_service,
    reply_service,
)
from DomainService import match_service


class ReplyMatchesUseCase:
    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
        
        if len(archived_matches) == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return

        reply_service.add_message(
            'このトークルームで行われた結果を表示します。第N回の詳細は「_match N」')
        
        match_details = []
        for i, match in enumerate(archived_matches):
            match_details.append(f'第{i+1}回 {match.created_at.strftime("%Y-%m-%d")}')
    
        reply_service.add_message('\n'.join(match_details))
