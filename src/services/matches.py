"""matches"""

from models import Matches, Results
from sqlalchemy import and_
import json
from db_setting import Session


class MatchesService:
    """matches service"""

    def __init__(self, services):
        self.services = services

    def get_current(self):
        room_id = self.services.app_service.req_room_id
        session = Session()
        return session\
            .query(Matches).filter(and_(
                Matches.room_id == room_id,
                Matches.status == 1
            )).order_by(Matches.id.desc())\
            .first()

    def get_or_add_current(self):
        """get or add"""
        current = self.get_current()

        if current is None:
            room_id = self.services.app_service.req_room_id
            current = Matches(room_id=room_id)
            session.add(current)
            session.commit()
            self.services.app_service.logger.info(f'create: room_id={room_id}')
        return current

    def add_result(self):
        """add result"""
        current_result = self.services.results_service.get_current()
        current_match = self.get_or_add_current()
        result_ids = json.loads(current_match.result_ids)
        result_ids.append(str(current_result.id))
        current_match.result_ids = json.dumps(result_ids)
        session.commit()
        self.services.app_service.logger.info(f'update: id={current_match.id}')

    def drop_result_by_number(self, i):
        """drop result"""

        if self.count_results() == 0:
            self.services.app_service.logger.warning(
                'current match is not found'
            )
            self.services.reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return

        current = self.get_current()
        result_ids = json.loads(current.result_ids)
        self.services.results_service.delete_by_id(result_ids[i-1])
        result_ids.pop(i-1)
        current.result_ids = json.dumps(result_ids)
        session.commit()
        self.services.app_service.logger.info(
            f'delete result: match_id={current.id} result_id={i-1}'
        )

    def count_results(self):
        current = self.get_current()
        if current is None:
            return 0
        return len(json.loads(current.result_ids))

    def get_sum_results(self):
        current = self.get_current()
        return self.services.results_service.get_sum_result_by_ids(
            json.loads(current.result_ids)
        )

    def reply_sum_results(self, match_id=None):
        print('hoge')
        if match_id is None:
            if self.count_results() == 0:
                self.services.reply_service.add_message(
                    'まだ対戦結果がありません。メニューの結果入力を押して結果を追加してください。')
                return
            match = self.get_current()
        else:
            session = Session()
            match = session\
                .query(Matches).filter(
                    Matches.id == match_id,
                ).first()
        self.services.results_service.reply_by_ids(
            json.loads(match.result_ids),
            date=match.created_at.strftime('%Y-%m-%d')+'\n',
        )

    def finish(self):
        if self.count_results() == 0:
            self.services.reply_service.add_message(
                'まだ対戦結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        current = self.get_current()
        self.services.results_service.reply_sum_and_money_by_ids(
            json.loads(current.result_ids),
            current.id,
        )
        self.archive()

    def archive(self):
        current = self.get_current()
        current.status = 2
        session.commit()
        self.services.app_service.logger.info(f'archive: id={current.id}')

    def disable(self):
        match = self.get_current()
        if match is None:
            return
        match.status = 0
        session.commit()
        self.services.app_service.logger.info(f'disable: id={match.id}')

    def reply(self):
        room_id = self.services.app_service.req_room_id
        matches = session\
            .query(Matches).filter(and_(
                Matches.status == 2,
                Matches.room_id == room_id,
            )).order_by(Matches.id.desc())\
            .all()
        if len(matches) == 0:
            self.services.reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return
        self.services.reply_service.add_message(
            '最近の4試合の結果を表示します。詳細は「_match <ID>」')
        for match in matches[:4]:
            self.services.results_service.reply_sum_and_money_by_ids(
                json.loads(match.result_ids),
                match.id,
                is_required_sum=False,
                date=match.created_at.strftime('%Y-%m-%d')+'\n'
            )

    def get(self, target_ids=None):
        if target_ids is None:
            return session\
                .query(Matches)\
                .order_by(Matches.id)\
                .all()
        if type(target_ids) != list:
            target_ids = [target_ids]
        return session\
            .query(Matches).filter(Matches.id.in_(target_ids))\
            .order_by(Matches.id).all()

    def remove_result_id(self, match_id, result_id):
        match = session\
            .query(Matches).filter(
                Matches.id == match_id
            ).first()
        result_ids = json.loads(match.result_ids)
        if result_id in result_ids:
            result_ids.remove(result_id)
        match.result_ids = json.dumps(result_ids)
        session.commit()

    def delete(self, target_ids):
        if type(target_ids) != 'list':
            target_ids = [target_ids]
        targets = session\
            .query(Matches).filter(
                Matches.id.in_(target_ids),
            ).all()
        for target in targets:
            self.services.results_service.delete(
                json.loads(target.result_ids)
            )
            session.delete(target)
        session.commit()
        self.services.app_service.logger.info(f'delete: id={target_ids}')

    def reply_sum_matches_by_ids(self, ids):
        formatted_id_list = sorted(list(set(ids)))
        room_id = self.services.app_service.req_room_id
        matches = session\
            .query(Matches).filter(and_(
                Matches.id.in_(ids),
                # Matches.room_id == room_id
            )).order_by(Matches.id)\
            .all()
        if len(matches) == 0:
            self.services.reply_service.add_message(
                '該当する対戦結果がありません。'
            )
            return
        self.services.reply_service.add_message(
            f'対戦ID={",".join(formatted_id_list)}の累計を表示します。'
        )
        result_ids = []
        for match in matches:
            result_ids += json.loads(match.result_ids)
        self.services.results_service.reply_sum_and_money_by_ids(
            result_ids,
            ','.join(formatted_id_list),
            is_required_sum=False,
        )

    # def plot(self):
        # room_id = self.services.app_service.req_room_id¥
        # room_id = 'R808c3c802d36f386290630fc6ba10f0c'
        # matches = session\
        # .query(Matches).filter(and_(
        ## Matches.status == 2,
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
        # self.services.reply_service.add_image(image_url)
