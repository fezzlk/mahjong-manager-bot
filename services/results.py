"""results"""

import json
from models import Results
from sqlalchemy import and_


class ResultsService:
    """Result service"""

    def __init__(self, services):
        self.services = services

    def add(self):
        """add"""

        room_id = self.services.app_service.req_room_id
        current_match = self.services.matches_service.get_or_add_current(
            room_id
        )
        result = Results(
            room_id=room_id,
            match_id=current_match.id,
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

    def reply_current_result(self):
        room_id = self.services.app_service.req_room_id
        results = self.services.room_service.rooms[room_id]['results']
        self.services.reply_service.add_text(f'一半荘お疲れ様でした。結果を表示します。')
        self.services.reply_service.add_text(
            '\n'.join([f'{user}: {point}' for user, point in results[-1].items()]))
        self.services.reply_service.add_text('今回の結果に一喜一憂せず次の戦いに望んでください。')

    def count(self):
        room_id = self.services.app_service.req_room_id
        results = self.services.room_service.rooms[room_id]['results']
        return len(results)

    def reset(self):
        room_id = self.services.app_service.req_room_id
        self.services.room_service.rooms[room_id]['results'] = []
        self.services.reply_service.add_text('今回の対戦結果を全て削除しました。')

    def reply_all(self):
        room_id = self.services.app_service.req_room_id
        results = self.services.room_service.rooms[room_id]['results']
        count = self.count()
        if count == 0:
            self.services.reply_service.add_text(
                'まだ結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        self.services.reply_service.add_text(
            'これまでの対戦結果です。(結果を指定して取り消したい場合は _delete, 全削除したい場合は _reset)')
        for i in range(count):
            self.services.reply_service.add_text(
                f'第{i+1}回\n'
                + '\n'.join([f'{user}: {point}' for user, point in results[i].items()]))
        sum = self.get_sum()
        self.services.reply_service.add_text(
            '総計\n' + '\n'.join([f'{user}: {point}' for user, point in sum.items()]))

    def finish(self):
        room_id = self.services.app_service.req_room_id
        results = self.services.room_service.rooms[room_id]['results']
        count = self.count()
        if count == 0:
            self.services.reply_service.add_text(
                'まだ結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        self.services.matches_service.add(results)
        self.services.reply_service.add_text('今回の総計を表示します。')
        self.reply_sum_and_money()

    def reply_sum_and_money(self, results=None):
        if results == None:
            room_id = self.services.app_service.req_room_id
            results = self.services.room_service.rooms[room_id]['results']
            results = results
        sum = self.get_sum(results)
        self.services.reply_service.add_text(
            '\n'.join([f'{user}: {point}' for user, point in sum.items()]))
        self.services.reply_service.add_text('\n'.join(
            [f'{user}: {point * self.services.config_service.get_rate()}円'
                for user, point in sum.items()]))

    def get_sum(self, results=None):
        if results == None:
            room_id = self.services.app_service.req_room_id
            results = self.services.room_service.rooms[room_id]['results']
            results = results
        sum_result = {}
        for res in results:
            for name, point in res.items():
                if not name in sum_result.keys():
                    sum_result[name] = 0
                sum_result[name] += point
        return sum_result

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
            )).first()

    def add_point(self, name, point):
        result = self.services.results_service.get_current()
        points = json.loads(result.points)
        points[name] = point
        result.points = json.dumps(points)
        self.services.app_service.db.session.commit()
        return result
