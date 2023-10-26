from ApplicationService import (
    request_info_service,
    reply_service,
    graph_service,
)
from DomainService import (
    hanchan_service,
    user_service,
    match_service,
)
from typing import Dict, Optional
import env_var


class ReplyMatchGraphUseCase:

    def execute(self, str_index: Optional[str] = None) -> None:
        line_group_id = request_info_service.req_line_group_id
        if str_index is None or str_index == '':
            target_match = match_service.find_latest_one(line_group_id)
            if target_match is None:
                reply_service.add_message(
                    'まだ対戦結果がありません。'
                )
                return
        else:
            if not str_index.isdigit():
                reply_service.add_message(
                    '引数は整数で指定してください。'
                )
                return

            archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
            index = int(str_index)
            if index < 1 or len(archived_matches) < index:
                reply_service.add_message(
                    f'このトークルームには全{len(archived_matches)}回までしか登録されていないため第{index}回はありません。'
                )
                return
            target_match = archived_matches[index-1]
        
        hanchans = hanchan_service.find_all_archived_by_match_id(target_match._id)
        line_id_list, score_plot_dict = graph_service.create_users_point_plot_data(
            hanchans=hanchans,
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
            upload_file_path=f'/match_detail/{str(target_match._id)}.png',
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
