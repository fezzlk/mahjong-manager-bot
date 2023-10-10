from ApplicationService import (
    request_info_service,
    reply_service,
)
from DomainService import (
    hanchan_service,
    user_service,
    match_service,
)
import env_var
from typing import Dict, Optional


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
        line_id_name_dict: Dict[str, str] = {}
        total_score_dict = {}
        score_plot_dict = {}
        for hanchan in hanchans:
            for line_id in hanchan.converted_scores:
                if line_id not in line_id_name_dict:
                    user = user_service.find_one_by_line_user_id(line_id)
                    if user is None:
                        continue
                    line_id_name_dict[user.line_user_id] = user.line_user_name
                    total_score_dict[line_id] = 0
                    score_plot_dict[line_id] = [0]
  
        for hanchan in hanchans:
            for line_id in line_id_name_dict:
                if line_id in hanchan.converted_scores:
                    total_score_dict[line_id] += hanchan.converted_scores[line_id]
                score_plot_dict[line_id].append(total_score_dict[line_id])


        # グラフ描画
        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MaxNLocator
        matplotlib.use('agg')

 
        fig, ax = plt.subplots()
        for line_id in line_id_name_dict:
            plt.plot(
                range(len(score_plot_dict[line_id])),
                score_plot_dict[line_id],
                label=line_id_name_dict[line_id])
            
        plt.grid(which='major', axis='y')
        plt.legend()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        try:
            fig.savefig(f"src/uploads/match_detail/{str(target_match._id)}.png")
        except FileNotFoundError:
            reply_service.reset()
            reply_service.add_message(text='システムエラーが発生しました。')
            messages = [
                '対戦履歴の画像アップロードに失敗しました',
                '送信者: ' + (user_service.get_name_by_line_user_id(request_info_service.req_line_user_id) or request_info_service.req_line_user_id),
            ]
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message='\n'.join(messages),
            )
            return
        plt.clf()
        plt.close()

        path = f'uploads/match_detail/{str(target_match._id)}.png'
        image_url = f'{env_var.SERVER_URL}{path}'
        reply_service.add_image(image_url)
