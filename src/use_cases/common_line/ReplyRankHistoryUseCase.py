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


class ReplyRankHistoryUseCase:
    def execute(self) -> None:
        req_line_user_id = request_info_service.req_line_user_id
        user_hanchans = user_hanchan_service.find_all_each_line_user_id(line_user_ids=[req_line_user_id])
            
        rank_info = [0, 0, 0, 0]
        if len(user_hanchans) != 0:
            for key, group in groupby(user_hanchans, key=lambda uh: uh.rank):
                rank_info[key-1] = len(list(group))/len(user_hanchans)
        reply_service.add_message('\n'.join([f'{i+1}着: {x:.2%}' for i, x in enumerate(rank_info)]))
        
        # プロットデータ作成
        plot_data = []
        for uh in user_hanchans[-10:]:
            plot_data.append(uh.rank)

        # グラフ描画
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.use('agg')

        fig, ax = plt.subplots()
        plt.plot(
            range(1, len(plot_data) + 1),
            plot_data,
            marker='o',
            clip_on=False)
        plt.grid(which='major', axis='y')
        plt.xticks(range(1, 11))
        plt.yticks(range(1, 5))
        plt.tick_params(labelbottom=False)
        ax.set_xlim([1, 10])
        ax.set_ylim([1, 4])
        ax.invert_yaxis()

        path = f'/rank_history/{req_line_user_id}.png'
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
