from ApplicationService import (
    message_service,
    reply_service,
    request_info_service,
)
from DomainService import (
    hanchan_service,
    match_service,
)
from use_cases.group_line.CreateMatchDetailGraphUseCase import (
    CreateMatchDetailGraphUseCase,
)


class ReplyMatchByIndexUseCase:
    def execute(self, str_index: str) -> None:
        line_group_id = request_info_service.req_line_group_id
        archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
        if not str_index.isdigit():
            reply_service.add_message(
                "引数は整数で指定してください。",
            )
            return

        index = int(str_index)
        if index < 1 or len(archived_matches) < index:
            reply_service.add_message(
                f"このトークルームには全{len(archived_matches)}回までしか登録されていないため第{index}回はありません。",
            )
            return

        match = archived_matches[index-1]
        result = message_service.create_show_match_result(match=match)

        reply_service.add_message(f'第{index}回\n{match.created_at.strftime("%Y年%m月%d日")}\n{result}')

        # 半荘情報
        hanchans = hanchan_service.find_all_archived_by_match_id(match._id)
        results_view_list = []
        sum_scores = {}
        for i, hanchan in enumerate(hanchans):
            for u, s in hanchan.converted_scores.items():
                if u in sum_scores:
                    sum_scores[u] += s
                else:
                    sum_scores[u] = s
            results_view_list.append(
                f"第{i+1}回\n{message_service.create_show_converted_scores(hanchan.converted_scores, sum_scores)}",
            )

        reply_service.add_message("【半荘情報】\n\n" + "\n\n".join(results_view_list))

        # グラフ描画
        reply_service.add_image(CreateMatchDetailGraphUseCase().execute(match._id))
