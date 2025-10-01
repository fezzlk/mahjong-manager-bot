from typing import Dict

from bson.objectid import ObjectId

import env_var
from ApplicationService import (
    graph_service,
    reply_service,
    request_info_service,
)
from DomainService import (
    hanchan_service,
    user_service,
)


class CreateMatchDetailGraphUseCase:

    def execute(self, match_id: ObjectId) -> str:
        hanchans = hanchan_service.find_all_archived_by_match_id(match_id)
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
            upload_file_path=f"/match_detail/{match_id!s}.png",
        )
        if err_message is not None:
            reply_service.reset()
            reply_service.add_message(text="システムエラーが発生しました。")
            messages = [
                err_message,
                "送信者: " + (user_service.get_name_by_line_user_id(request_info_service.req_line_user_id) or request_info_service.req_line_user_id),
            ]
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message="\n".join(messages),
            )
            return None
        return image_url
