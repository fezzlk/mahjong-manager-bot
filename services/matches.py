"""matches"""

from models import Matches
from sqlalchemy import and_
import json


class MatchesService:
    """matches service"""

    def __init__(self, services):
        self.services = services

    def get_or_add_current(self, room_id=None):
        """get or add"""
        if room_id is None:
            room_id = self.services.app_service.req_room_id
        current = self.services.app_service.db.session\
            .query(Matches).filter(and_(
                Matches.room_id == room_id,
                Matches.status == 1
            )).first()

        if current == None:
            current = Matches(room_id=room_id)
            self.services.app_service.db.session.add(current)
            self.services.app_service.db.session.commit()
        return current

    def add_result(self):
        """add result"""
        current_result = self.services.results_service.get_current()
        current_match = self.get_or_add_current()
        result_ids = current_match.result_ids.split(',')
        if result_ids[0] == '':
            result_ids[0] = str(current_result.id)
        else:
            result_ids.append(str(current_result.id))
        current_match.result_ids = ','.join(result_ids)
        self.services.app_service.db.session.commit()
        self.services.results_service.archive()

    def drop(self, i):
        if len(self.matches) > i:
            self.matches.pop(i)

    def reset(self):
        self.results = []
        self.services.reply_service.add_text('結果を全て削除しました。')

    def count_results(self):
        room_id = self.services.app_service.req_room_id
        match = self.services.app_service.db.session\
            .query(Matches).filter(and_(
                Matches.room_id == room_id,
                Matches.status == 1,
            )).first()
        ids = match.result_ids.split(',')
        if ids[0] == '':
            return 0
        else:
            return len(ids)

    def reply_all(self):
        if self.count() == 0:
            self.services.reply_service.add_text(
                'まだ対戦結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        self.services.reply_service.add_text(
            'これまでの対戦結果です。(結果を指定して取り消したい場合は _delete_m, 全削除したい場合は _reset_m)')

        for i, match in enumerate(self.matches):
            self.services.reply_service.add_text(f'第{i+1}回')
            self.services.results_service.reply_sum_and_money(match)
