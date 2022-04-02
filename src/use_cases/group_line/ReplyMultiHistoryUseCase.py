from datetime import datetime
from typing import Dict, List
from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    user_match_repository,
    user_repository,
    match_repository,
    hanchan_repository,
    session_scope,
)
import env_var
import itertools

# flake8: noqa
import japanize_matplotlib


class ReplyMultiHistoryUseCase:

    def execute(self, user_names: List[str]) -> None:
        req_line_id = request_info_service.req_line_user_id
        messages = []
        um_total: List[UserMatch] = []
        user_line_ids: List[str] = []
        line_id_name_dict: Dict[str, str] = {}

        with session_scope() as session:
            for user_name in user_names:
                users = user_repository.find_by_name(
                    session,
                    user_name,
                )

                if len(users) == 0:
                    messages.append(f'{user_name} は登録されていません。')
                    continue
                elif len(users) > 1:
                    messages.append(f'{user_name} は複数存在しています。(1人分だけ出します')

                user = users[0]
                line_id_name_dict[user.line_user_id] = user_name
                user_line_ids.append(user.line_user_id)
                um_total += user_match_repository.find_by_user_ids(
                    session,
                    [user._id],
                )

            matches = match_repository.find_archived_by_ids(
                session,
                [um.match_id for um in um_total]
            )

            if len(matches) == 0:
                reply_service.add_message(
                    '対局履歴がありません。'
                )
                return

            all_hanchan_ids = list(
                itertools.chain.from_iterable(
                    [m.hanchan_ids for m in matches]
                )
            )

            all_hanchans = hanchan_repository.find_archived_by_ids(
                session,
                all_hanchan_ids,
            )

            if len(all_hanchans) == 0:
                raise ValueError('半荘情報を取得できませんでした。')

            dict_c_results = {h._id: h.converted_scores for h in all_hanchans}

            message = ''
            total_dict = {line_id: 0 for line_id in user_line_ids}
            history_dict = {line_id: [
                [datetime(2021, 2, 1)], [0]] for line_id in user_line_ids}

            for line_id in user_line_ids:
                for match in matches:
                    score = 0
                    for hanchan_id in match.hanchan_ids:
                        if hanchan_id in dict_c_results:
                            if line_id in dict_c_results[hanchan_id]:
                                score += dict_c_results[hanchan_id][line_id]
                    total_dict[line_id] += score
                    history_dict[line_id][0].append(match.created_at)
                    history_dict[line_id][1].append(total_dict[line_id])

            import matplotlib.pyplot as plt
            fig = plt.figure()
            plt.xlim([datetime(2021, 2, 1), datetime.today()])

            for line_id in user_line_ids:
                plt.step(
                    history_dict[line_id][0],
                    history_dict[line_id][1],
                    where='post',
                    label=line_id_name_dict[line_id])
            plt.legend()

            try:
                fig.savefig(f"src/uploads/group_history/{req_line_id}.png")
            except FileNotFoundError:
                reply_service.reset()
                reply_service.add_message(text='システムエラーが発生しました。')
                messages = [
                    '対戦履歴の画像アップロードに失敗しました',
                    '送信者: ' + req_line_id,
                ]
                reply_service.push_a_message(
                    to=env_var.SERVER_ADMIN_LINE_USER_ID,
                    message='\n'.join(messages),
                )
                return
            plt.clf()
            plt.close()

            path = f'uploads/group_history/{req_line_id}.png'
            image_url = f'{env_var.SERVER_URL}{path}'
            reply_service.add_image(image_url)

            reply_service.add_message(
                message
            )
