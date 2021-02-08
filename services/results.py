"""results"""

import json
from models import Results
from sqlalchemy import and_, desc


class ResultsService:
    """Result service"""

    def __init__(self, services):
        self.services = services

    def add(self, points={}):
        """add"""

        room_id = self.services.app_service.req_room_id
        current_match = self.services.matches_service.get_or_add_current(
            room_id
        )
        result = Results(
            room_id=room_id,
            match_id=current_match.id,
            points=points,
        )
        self.services.app_service.db.session.add(result)
        self.services.app_service.db.session.commit()

    def update(self, result):
        self.services.app_service.db.session.add(result)
        self.services.app_service.db.session.commit()

    def drop(self, i):
        room_id = self.services.app_service.req_room_id
        results = self.services.room_service.rooms[room_id]['results']
        if self.count() > i:
            results.pop(i)

    def drop_by_id(self, target_id):
        room_id = self.services.app_service.req_room_id
        target = self.services.app_service.db.session\
            .query(Results).filter(and_(
                Results.room_id == room_id,
                Results.id == target_id,
            )).first()
        target.status = 0
        self.services.app_service.db.session.commit()
        self.services.reply_service.add_text(f'id={target_id}の結果を削除しました。')

    def reply_current_result(self):
        result = self.services.results_service.get_current()
        calculated_result = json.loads(result.result)
        self.services.reply_service.add_text(f'一半荘お疲れ様でした。結果を表示します。')
        self.services.reply_service.add_text(
            '\n'.join([f'{user}: {point}' for user, point in calculated_result.items()]))
        self.services.reply_service.add_text('今回の結果に一喜一憂せず次の戦いに望んでください。')

    def count(self):
        room_id = self.services.app_service.req_room_id
        results = self.services.room_service.rooms[room_id]['results']
        return len(results)

    def reset(self):
        room_id = self.services.app_service.req_room_id
        self.services.room_service.rooms[room_id]['results'] = []
        self.services.reply_service.add_text('今回の対戦結果を全て削除しました。')

    def reply_all_by_ids(self, ids):
        results = self.services.app_service.db.session\
            .query(Results).filter(
                Results.id.in_([int(s) for s in ids]),
            )\
            .order_by(Results.id)\
            .all()
        results_list = []
        sum_results = {}
        for i in range(len(ids)):
            result = json.loads(results[i].result)
            results_list.append(
                f'第{i+1}回\n' + '\n'.join(
                    [f'{user}: {point}' for user, point in result.items()]
                )
            )
            for name, point in result.items():
                if not name in sum_results.keys():
                    sum_results[name] = 0
                sum_results[name] += point
        self.services.reply_service.add_text('\n\n'.join(results_list))
        self.services.reply_service.add_text(
            '総計\n' + '\n'.join(
                [f'{user}: {point}' for user, point in sum_results.items()]
            )
        )

    def reply_sum_and_money_by_ids(self, ids, is_rep_sum=True, date=''):
        results = self.services.app_service.db.session\
            .query(Results).filter(
                Results.id.in_([int(s) for s in ids]),
            ).all()
        sum_results = {}
        for i in range(len(ids)):
            result = json.loads(results[i].result)
            for name, point in result.items():
                if not name in sum_results.keys():
                    sum_results[name] = 0
                sum_results[name] += point
        if is_rep_sum:
            self.services.reply_service.add_text(
                '\n'.join([f'{user}: {point}' for user, point in sum_results.items()]))
        key = 'レート'
        self.services.reply_service.add_text(date + '\n'.join(
            [f'{user}: {point * int(self.services.config_service.get_by_key(key)[1]) * 10}円'
             for user, point in sum_results.items()]))

    def delete_by_text(self, text):
        if text.isdigit() == False:
            self.services.reply_service.add_text('数字で指定してください。')
            return
        i = int(text)
        if 0 < i & self.services.results_service.count() <= i:
            self.services.results_service.drop(i-1)
            self.services.reply_service.add_text(f'{i}回目の結果を削除しました。')
            return
        self.services.reply_service.add_text('指定された結果が存在しません。')

    def get_current(self):
        room_id = self.services.app_service.req_room_id
        return self.services.app_service.db.session\
            .query(Results).filter(and_(
                Results.room_id == room_id,
                Results.status == 1,
            ))\
            .order_by(desc(Results.id))\
            .first()

    def add_point(self, name, point):
        result = self.services.results_service.get_current()
        points = json.loads(result.points)
        points[name] = point
        result.points = json.dumps(points)
        self.services.app_service.db.session.commit()
        return points

    def drop_point(self, name):
        result = self.services.results_service.get_current()
        points = json.loads(result.points)
        if name in points.keys():
            points.pop(name)
        result.points = json.dumps(points)
        self.services.app_service.db.session.commit()
        return points

    def reset_points(self):
        result = self.services.results_service.get_current()
        result.points = json.dumps({})
        self.services.app_service.db.session.commit()

    def update_result(self, calculated_result):
        result = self.services.results_service.get_current()
        result.result = json.dumps(calculated_result)
        self.services.app_service.db.session.commit()

    def archive(self):
        result = self.services.results_service.get_current()
        result.status = 2
        self.services.app_service.db.session.commit()

    def drop_active(self):
        room_id = self.services.app_service.req_room_id
        self.services.app_service.db.session\
            .query(Results).filter(and_(
                Results.room_id == room_id,
                Results.status == 1,
            ))\
            .delete()
        self.services.app_service.db.session.commit()

    def get_all(self):
        results = self.services.app_service.db.session\
            .query(Results)\
            .order_by(Results.id)\
            .all()
        for result in results:
            result.points = json.loads(result.points)
            result.result = json.loads(result.result)
        return results

    def delete(self, target_ids):
        if type(target_ids) != list:
            target_ids = [target_ids]
        targets = self.services.app_service.db.session\
            .query(Results).filter(
                Results.id.in_(target_ids),
            ).all()
        for target in targets:
            self.services.matches_service.remove_result_id(
                target.match_id, target.id)
            self.services.app_service.db.session.delete(target)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_ids}')
