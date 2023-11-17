from ApplicationService import (
    request_info_service,
    reply_service,
)
from DomainService import (
    user_service,
    user_hanchan_service,
)
import env_var
from itertools import groupby
from DomainModel.entities.UserHanchan import UserHanchan
from ApplicationService import message_service


class ReplyRankHistogramUseCase:
    def execute(self) -> None:
        req_line_user_id = request_info_service.req_line_user_id
        from_str = request_info_service.params.get('from')
        to_str = request_info_service.params.get('to')
        from_dt, from_is_invalid = message_service.parse_date_from_text(from_str)
        to_dt, to_is_invalid = message_service.parse_date_from_text(to_str)
        if from_is_invalid or to_is_invalid:
            reply_service.add_message('日付は以下のフォーマットで入力してください。')
            reply_service.add_message('[日付の入力方法]\n\nYYYY年MM月DD日\n→ YYYYMMDD\n\n20YY年MM月DD日\n→ YYMMDD\n\n今年MM月DD日\n→ MMDD\n\n今月DD日\n→ DD')
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
        for i in range(1,5):
            plot_data.append([uh.created_at for uh in user_hanchans if uh.rank == i])
            labels.append(f'{i}着')

        # グラフ描画
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        matplotlib.use('agg')

        fig, ax = plt.subplots()
        plt.hist(plot_data, label=labels)
        plt.grid(which='major', axis='y', linestyle="dotted")
        plt.xticks(rotation=30)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%y/%m/%d"))
        ax.set_axisbelow(True)
        plt.legend()

        path = f'/rank_histogram/{req_line_user_id}.png'
        try:
            fig.savefig(f"src/uploads{path}")
        except FileNotFoundError:
            reply_service.reset()
            reply_service.add_message(text='システムエラーが発生しました。')
            messages = [
                '順位履歴の画像アップロードに失敗しました',
                '送信者: ' + (user_service.get_name_by_line_user_id(request_info_service.req_line_user_id) or request_info_service.req_line_user_id),
            ]
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message='\n'.join(messages),
            )
            return
        
        plt.clf()
        plt.close()

        reply_service.add_image(f'{env_var.SERVER_URL}/uploads{path}')
