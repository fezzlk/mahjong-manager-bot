# flake8: noqa: E999
"""matches"""

import json
from server import logger
from services import (
    app_service,
    hanchans_service,
    reply_service,
    matches_service,
)


class MatchesUseCases:
    """matches use cases"""

    def drop_result_by_number(self, i):
        """drop result"""

        if matches_service.count_results() == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return
        current = matches_service.get_current()
        result_ids = json.loads(current.result_ids)
        hanchans_service.delete_by_id(result_ids[i - 1])
        result_ids.pop(i - 1)
        matches_service.update_hanchan_ids(result_ids)

    def reply_sum_results(self, match_id=None):
        if match_id is None:
            if matches_service.count_results() == 0:
                reply_service.add_message(
                    'まだ対戦結果がありません。')
                return
            match = matches_service.get_current()
        else:
            match = matches_service.get(match_id)

        hanchans_service.reply_by_ids(
            json.loads(match.result_ids),
            date=match.created_at.strftime('%Y-%m-%d') + '\n',
        )

    def finish(self):
        if matches_service.count_results() == 0:
            reply_service.add_message(
                'まだ対戦結果がありません。')
            return
        current = matches_service.get_current()
        hanchans_service.reply_sum_and_money_by_ids(
            json.loads(current.result_ids),
            current.id,
        )
        matches_service.archive()

    def reply(self):
        room_id = app_service.req_room_id
        matches = matches_service.get_archived(room_id)
        if matches is None:
            reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return

        reply_service.add_message(
            '最近の4試合の結果を表示します。詳細は「_match <ID>」')
        for match in matches[:4]:
            hanchans_service.reply_sum_and_money_by_ids(
                json.loads(match.result_ids),
                match.id,
                is_required_sum=False,
                date=match.created_at.strftime('%Y-%m-%d') + '\n'
            )

    def get(self, target_ids=None):
        matches_service.get(target_ids)

    def delete(self, target_ids):
        targets = matches_service.delete(target_ids)
        for target in targets:
            hanchans_service.delete(
                json.loads(target.result_ids)
            )
        logger.info(f'delete match: id={target_ids}')

    def reply_sum_matches_by_ids(self, ids):
        formatted_id_list = sorted(list(set(ids)))
        matches = matches_service.get(ids)
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
        hanchans_service.reply_sum_and_money_by_ids(
            result_ids,
            ','.join(formatted_id_list),
            is_required_sum=False,
        )

    # def plot(self):
        # room_id = app_service.req_room_id¥
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
