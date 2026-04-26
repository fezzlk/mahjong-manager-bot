import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from application_service import (
    graph_service,
    message_service,
    reply_service,
    request_info_service,
)
from domain_service import (
    user_hanchan_service,
    user_service,
)


class ReplyRankHistogramUseCase:
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

        # プロットデータ作成
        plot_data = []
        labels = []
        for i in range(1, 5):
            plot_data.append([uh.created_at for uh in user_hanchans if uh.rank == i])
            labels.append(f"{i}着")
        # 飛び
        plot_data.append([uh.created_at for uh in user_hanchans if uh.point < 0])
        labels.append("飛び")

        # グラフ描画
        fig, ax = plt.subplots()
        plt.hist(plot_data, label=labels)
        plt.grid(which="major", axis="y", linestyle="dotted")
        plt.xticks(rotation=30)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%y/%m/%d"))
        ax.set_axisbelow(True)
        plt.legend()

        path = f"/rank_histogram/{req_line_user_id}.png"
        url, err = graph_service.save_figure(fig, path)
        if err:
            sender = (
                user_service.get_name_by_line_user_id(req_line_user_id)
                or req_line_user_id
            )
            reply_service.create_and_reply_file_upload_error("順位履歴", sender)
            return
        reply_service.add_image(url)
