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
        current_match = self.services.matches_service.get_or_add_current()
        result = Results(
            room_id=room_id,
            match_id=current_match.id,
            points=points,
        )
        self.services.app_service.db.session.add(result)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'create: room_id={room_id}')

    def delete_by_id(self, target_id):
        room_id = self.services.app_service.req_room_id
        target = self.services.app_service.db.session\
            .query(Results).filter(and_(
                Results.room_id == room_id,
                Results.id == target_id,
            )).first()
        target.status = 0
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_id} room_id={room_id}')
        self.services.reply_service.add_message(f'id={target_id}の結果を削除しました。')

    def reply_current_result(self):
        result = self.get_current()
        calculated_result = json.loads(result.result)
        sum_results = self.services.matches_service.get_sum_results()
        self.services.reply_service.add_message(f'一半荘お疲れ様でした。結果を表示します。')
        self.services.reply_service.add_message(
            '\n'.join([
                f'{r[0]}: {"+" if r[1] > 0 else ""}{r[1]} ({"+" if sum_results[r[0]] > 0 else ""}{sum_results[r[0]]})'
                for r in sorted(calculated_result.items(), key=lambda x:x[1], reverse=True)
            ])
        )
        self.services.reply_service.add_message(
            self.services.message_service.get_result_message())

    def get_sum_result_by_ids(self, ids):
        results = self.services.app_service.db.session\
            .query(Results).filter(
                Results.id.in_([int(s) for s in ids]),
            )\
            .order_by(Results.id)\
            .all()
        sum_results = {}
        for r in results:
            res_obj = json.loads(r.result)
            print(res_obj)
            for name, point in res_obj.items():
                if not name in sum_results.keys():
                    sum_results[name] = 0
                sum_results[name] += point
        return sum_results

    def reply_by_ids(self, ids):
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
                    [f'{r[0]}: {"+" if r[1] > 0 else ""}{r[1]}' for r in sorted(result.items(), key=lambda x:x[1], reverse=True)]
                )
            )
            for name, point in result.items():
                if not name in sum_results.keys():
                    sum_results[name] = 0
                sum_results[name] += point
        self.services.reply_service.add_message('\n\n'.join(results_list))
        self.services.reply_service.add_message(
            '総計\n' + '\n'.join(
                [f'{r[0]}: {"+" if r[1] > 0 else ""}{r[1]}' for r in sorted(sum_results.items(), key=lambda x:x[1], reverse=True)]
            )
        )

    def reply_sum_and_money_by_ids(self, ids, match_id, is_required_sum=True, date=''):
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
        if is_required_sum:
            self.services.reply_service.add_message(
                '\n'.join([f'{user}: {point}' for user, point in sum_results.items()]))
        key = 'レート'
        self.services.reply_service.add_message('対戦ID: ' + str(match_id) + '\n' + date + '\n'.join(
            [f'{user}: {point * int(self.services.config_service.get_by_key(key)[1]) * 10}円'
             for user, point in sum_results.items()]))

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
        result = self.get_current()
        points = json.loads(result.points)
        points[name] = point
        result.points = json.dumps(points)
        self.services.app_service.db.session.commit()
        return points

    def drop_point(self, name):
        result = self.get_current()
        points = json.loads(result.points)
        if name in points.keys():
            points.pop(name)
        result.points = json.dumps(points)
        self.services.app_service.db.session.commit()
        return points

    def reset_points(self):
        result = self.get_current()
        result.points = json.dumps({})
        self.services.app_service.db.session.commit()

    def update_result(self, calculated_result):
        result = self.get_current()
        result.result = json.dumps(calculated_result)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'update result: id={result.id}')

    def archive(self):
        current = self.get_current()
        if current is None:
            return
        current.status = 2
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'archive: id={current.id}')

    def disable(self):
        current = self.get_current()
        if current is None:
            return
        current.status = 0
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'disable: id={current.id}')

    def get(self, target_ids=None):
        if target_ids is None:
            targets = self.services.app_service.db.session\
                .query(Results)\
                .order_by(Results.id)\
                .all()
        else:
            if type(target_ids) != list:
                target_ids = [target_ids]
            targets = self.services.app_service.db.session\
                .query(Results).filter(Results.id.in_(target_ids))\
                .order_by(Results.id).all()
        for result in targets:
            if result.points is not None:
                result.points = json.loads(result.points)
            if result.result is not None:
                result.result = json.loads(result.result)
        return targets

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
