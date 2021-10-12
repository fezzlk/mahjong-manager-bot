# flake8: noqa: E999
"""matches"""

import json
from server import logger
from services import (
    request_info_service,
    hanchan_service,
    reply_service,
    match_service,
)


class MatchesUseCases:
    """matches use cases"""

    def drop_result_by_number(self, i):
        """drop result"""

        if match_service.count_results() == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return
        current = match_service.get_current()
        result_ids = json.loads(current.result_ids)
        room_id = request_info_service.req_line_room_id
        hanchan_service.delete_by_id(room_id, result_ids[i - 1])
        reply_service.add_message(
            f'id={target_id}の結果を削除しました。'
        )
        result_ids.pop(i - 1)
        match_service.update_hanchan_ids(result_ids)

    def reply_sum_results(self, match_id=None):
        if match_id is None:
            if match_service.count_results() == 0:
                reply_service.add_message(
                    'まだ対戦結果がありません。')
                return
            match = match_service.get_current()
        else:
            match = match_service.get(match_id)

        ids = json.loads(match.result_ids)
        date = match.created_at.strftime('%Y-%m-%d') + '\n',
        hanchans = hanchan_service.find_by_ids(ids)

        hanchans_list = []
        sum_hanchans = {}

        for i in range(len(ids)):
            converted_scores = json.loads(hanchans[i].converted_scores)
            hanchans_list.append(
                f'第{i+1}回\n' + '\n'.join([
                    f'{user_service.get_name_by_line_user_id(r[0])}: \
                        {"+" if r[1] > 0 else ""}{r[1]}'
                    for r in sorted(
                        converted_scores.items(),
                        key=lambda x:x[1],
                        reverse=True
                    )
                ])
            )

            for user_id, converted_score in converted_scores.items():
                if user_id not in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0

                sum_hanchans[user_id] += converted_score

        reply_service.add_message('\n\n'.join(hanchans_list))
        reply_service.add_message(
            '総計\n' + date + '\n'.join([
                f'{user_service.get_name_by_line_user_id(r[0])}: \
                    {"+" if r[1] > 0 else ""}{r[1]}'
                for r in sorted(
                    sum_hanchans.items(),
                    key=lambda x:x[1],
                    reverse=True
                )
            ])
        )

    def finish(self):
        if match_service.count_results() == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return
        current = match_service.get_current()
        self.reply_sum_and_money_by_ids(
            json.loads(current.result_ids),
            current.id,
        )
        match_service.archive()

    def reply(self):
        room_id = request_info_service.req_line_room_id
        matches = match_service.get_archived(room_id)
        if matches is None:
            reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return

        reply_service.add_message(
            '最近の4試合の結果を表示します。詳細は「_match <ID>」')
        for match in matches[:4]:
            self.reply_sum_and_money_by_ids(
                json.loads(match.result_ids),
                match.id,
                is_required_sum=False,
                date=match.created_at.strftime('%Y-%m-%d') + '\n'
            )

    def get(self, target_ids=None):
        match_service.get(target_ids)

    def delete(self, target_ids):
        targets = match_service.delete(target_ids)
        for target in targets:
            hanchan_service.delete(
                json.loads(target.result_ids)
            )
        logger.info(f'delete match: id={target_ids}')

    def reply_sum_matches_by_ids(self, ids):
        formatted_id_list = sorted(list(set(ids)))
        matches = match_service.get(ids)
        if len(matches) == 0:
            reply_service.add_message(
                '該当する対戦結果がありません。'
            )
            return
        reply_service.add_message(
            f'対戦ID={",".join(formatted_id_list)}の累計を表示します。'
        )
        result_ids = []
        for match in matches:
            result_ids += json.loads(match.result_ids)
        self.reply_sum_and_money_by_ids(
            result_ids,
            ','.join(formatted_id_list),
            is_required_sum=False,
        )

    def reply_sum_and_money_by_ids(
        self,
        ids,
        match_id,
        is_required_sum=True,
        date=''
    ):
        hanchans = hanchan_service.find_by_ids(ids)

        sum_hanchans = {}
        for i in range(len(ids)):
            converted_scores = json.loads(hanchans[i].converted_scores)

            for user_id, converted_score in converted_scores.items():
                if user_id not in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0
                sum_hanchans[user_id] += converted_score

        if is_required_sum:
            reply_service.add_message(
                '\n'.join([
                    f'{user_service.get_name_by_line_user_id(user_id)}: \
                        {converted_score}'
                    for user_id, converted_score in sum_hanchans.items()
                ])
            )

        key = 'レート'
        room_id = request_info_service.req_line_room_id
        reply_service.add_message(
            '対戦ID: ' + str(match_id) + '\n' + date + '\n'.join([
                f'{user_service.get_name_by_line_user_id(user_id)}: \
                {converted_score * int(config_service.get_value_by_key(room_id, key)[1]) * 10}円 \
                ({"+" if converted_score > 0 else ""}{converted_score})'
                for user_id, converted_score in sum_hanchans.items()
            ])
        )
    # def plot(self):
        # room_id = request_info_service.req_line_room_id¥
        # room_id = 'R808c3c802d36f386290630fc6ba10f0c'
        # matches = session\
        # .query(Matches).filter(and_(
        # Matches.status == 2,
        # Matches.room_id == room_id,
        # )).order_by(Matches.id.desc())\
        # .all()
        # match = matches[0]
        # print(match)
        # 以下ResultServiceに移植
        # results = session\
        # .query(Results).filter(
        # Results.id.in_([int(s) for s in json.loads(match.result_ids)]),
        # )\
        # .order_by(Results.id)\
        # .all()
        # x = []
        # y = pd.DataFrame({})
        # print(results)
        # for result in results:
        # y = y.append(pd.Series(json.loads(result.result), name=result.id))
        # print(y)
        # plt.figure()

        # # Data for plotting
        # t = np.arange(0.0, 2.0, 0.01)
        # s = 1 + np.sin(2 * np.pi * t)

        # fig, ax = plt.subplots()
        # ax.plot(t, s)

        # ax.set(xlabel='time (s)', ylabel='voltage (mV)',
        #        title='About as simple as it gets, folks')
        # ax.grid()
        # path = "static/images/graphs/fuga.png"

        # fig.savefig(path)
        # image_url = f'https://f4d896d5edd1.ngrok.io/{path}'
        # image_url = f'https://mahjong-manager.herokuapp.com/{path}'
        # reply_service.add_image(image_url)
