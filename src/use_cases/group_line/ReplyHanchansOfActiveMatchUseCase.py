from ApplicationService import (
    request_info_service,
    reply_service,
    message_service,
)
from DomainService import (
    group_service,
    hanchan_service,
)


class ReplyHanchansOfActiveMatchUseCase:
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

        archived_hanchans = hanchan_service.find_all_archived_by_match_id(match_id=group.active_match_id)

        if len(archived_hanchans) == 0:
            reply_service.add_message(
                '現在の対戦で登録済みの半荘がありません。'
            )
            return
        
        reply_service.add_message(
            '途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。')
        
        results_view_list = []
        sum_scores = {}
        for i, hanchan in enumerate(archived_hanchans):
            for u, s in hanchan.converted_scores.items():
                if u in sum_scores:
                    sum_scores[u] += s
                else:
                    sum_scores[u] = s
            results_view_list.append(
                f'第{i+1}回\n{message_service.create_show_converted_scores(hanchan.converted_scores, sum_scores)}'
            )
    
        reply_service.add_message('\n\n'.join(results_view_list))
