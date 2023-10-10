from ApplicationService import (
    request_info_service,
    reply_service,
)
from DomainService import (
    match_service,
    group_service,
    hanchan_service,
    user_service,
)

class ReplyActiveMatchDetailUseCase:
    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                'トークルームが登録されていません。招待し直してください。'
            )
            return
        if group.active_match_id is None:
            reply_service.add_message(
                '現在進行中の対戦がありません。'
            )
            return
        
        match = match_service.find_one_by_id(_id=group.active_match_id)
        if match is None:
            raise BaseException(f'ReplyActiveMatchDetailUseCase: 対戦結果の取得失敗: match_id{group.active_match_id}')

        archived_hanchans = hanchan_service.find_all_archived_by_match_id(match_id=match._id)
        
        hanchan_detail_list = []
        for i, hanchan in enumerate(archived_hanchans):
            score_text_list = []
            for r in sorted(
                hanchan.converted_scores.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                name = user_service.get_name_by_line_user_id(r[0]) or "友達未登録"
                score = ("+" if r[1] > 0 else "") + str(r[1])
                score_text_list.append(
                    f'{name}: {score}'
                )
            hanchan_detail_list.append(f'第{i}回\n' + '\n'.join(score_text_list))
            
        reply_service.add_message(
            '\n\n'.join(hanchan_detail_list)
        )