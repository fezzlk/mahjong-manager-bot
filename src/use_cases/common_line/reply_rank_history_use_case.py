from itertools import groupby

import matplotlib.pyplot as plt

from application_service import (
    graph_service,
    message_service,
    reply_service,
    request_info_service,
)
from domain_model.entities.user_hanchan import UserHanchan
from domain_service import (
    user_hanchan_service,
    user_service,
)


class ReplyRankHistoryUseCase:
    def execute(self) -> None:
        req_line_user_id = request_info_service.req_line_user_id
        from_dt, to_dt, is_valid = message_service.parse_date_range_from_params(
            request_info_service.params,
        )
        if not is_valid:
            for msg in message_service.DATE_FORMAT_ERROR_MESSAGES:
                reply_service.add_message(msg)
            return
        user_hanchans = user_hanchan_service.find_all_each_line_user_id(
            line_user_ids=[req_line_user_id],
            from_dt=from_dt,
            to_dt=to_dt,
        )

        range_message = message_service.create_range_message(from_dt, to_dt)
        if range_message is not None:
            reply_service.add_message(range_message)

        # 順位グラフ作成
        rank_info = [0, 0, 0, 0, 0]
        ave_rank = 0.0
        if len(user_hanchans) != 0:
            sum_rank = 0
            sorted_user_hanchans: list[UserHanchan] = sorted(
                user_hanchans,
                key=lambda x: x.rank,
                reverse=False,
            )
            for key, group in groupby(sorted_user_hanchans, key=lambda uh: uh.rank):
                count = len(list(group))
                rank_info[key - 1] = count / len(user_hanchans)
                sum_rank += count * key
            # 飛び率
            rank_info[4] = sum([h.point < 0 for h in user_hanchans]) / len(
                user_hanchans,
            )
            # 平均順位
            ave_rank = sum_rank / len(user_hanchans)

        fig, ax = plt.subplots()
        ax.set_title(f"平均順位: {ave_rank:.4}", loc="right")
        bar_chart = plt.bar(
            [f"{i + 1}着" for i in range(4)] + ["飛び"],
            rank_info,
            color=["#EA4060", "#41C9B3", "#3392BB", "#F8BA00", "#2E3441"],
        )
        ax.bar_label(bar_chart, labels=[f"{x:.2%}" for x in rank_info])
        plt.grid(which="major", axis="y")
        ax.set_axisbelow(True)
        path = f"/rank_bar_chart/{req_line_user_id}.png"
        url, err = graph_service.save_figure(fig, path)
        if err:
            sender = (
                user_service.get_name_by_line_user_id(req_line_user_id)
                or req_line_user_id
            )
            reply_service.create_and_reply_file_upload_error("順位履歴", sender)
            return
        reply_service.add_image(url)

        # プロットデータ作成
        plot_data = []
        for uh in user_hanchans[-10:]:
            plot_data.append(uh.rank)

        # グラフ描画
        fig, ax = plt.subplots()
        plt.plot(range(1, len(plot_data) + 1), plot_data, marker="o", clip_on=False)
        plt.grid(which="major", axis="y")
        plt.xticks(range(1, 11))
        plt.yticks(range(1, 5))
        plt.tick_params(labelbottom=False)
        ax.set_xlim([1, 10])
        ax.set_ylim([1, 4])
        ax.invert_yaxis()

        path = f"/rank_history/{req_line_user_id}.png"
        url, err = graph_service.save_figure(fig, path)
        if err:
            sender = (
                user_service.get_name_by_line_user_id(req_line_user_id)
                or req_line_user_id
            )
            reply_service.create_and_reply_file_upload_error("順位履歴", sender)
            return
        reply_service.add_image(url)
