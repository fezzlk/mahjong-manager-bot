from ApplicationService import (
    request_info_service,
    reply_service,
    message_service,
    graph_service,
)
from DomainService import (
    group_service,
    user_service,
    hanchan_service,
)
from typing import Dict
import env_var


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

        # グラフ描画
        line_id_list, score_plot_dict = graph_service.create_users_point_plot_data(
            hanchans=archived_hanchans,
        )
        line_id_name_dict: Dict[str, str] = {}
        for line_id in line_id_list:
            user = user_service.find_one_by_line_user_id(line_id)
            if user is None:
                continue
            line_id_name_dict[line_id] = user.line_user_name

        image_url, err_message = graph_service.create_users_point_plot_graph_url(
            line_id_name_dict=line_id_name_dict,
            plot_dict=score_plot_dict,
            upload_file_path=f'/group_active_match_detail/{line_group_id}.png',
        )
        if err_message is not None:
            reply_service.reset()
            reply_service.add_message(text='システムエラーが発生しました。')
            messages = [
                err_message,
                '送信者: ' + (user_service.get_name_by_line_user_id(request_info_service.req_line_user_id) or request_info_service.req_line_user_id),
            ]
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message='\n'.join(messages),
            )
            return
        reply_service.add_image(image_url)
