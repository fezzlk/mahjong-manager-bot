"""matches"""

from models import Matches
from sqlalchemy import and_
import json


class MatchesService:
    """matches service"""

    def __init__(self, services):
        self.services = services

    def get_current(self, room_id=None):
        if room_id is None:
            room_id = self.services.app_service.req_room_id
        return self.services.app_service.db.session\
            .query(Matches).filter(and_(
                Matches.room_id == room_id,
                Matches.status == 1
            )).order_by(Matches.id.desc())\
            .first()

    def get_or_add_current(self, room_id=None):
        """get or add"""
        current = self.get_current(room_id)

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

    def drop_result_by_time(self, i):
        """drop result"""
        if self.count_results() == 0:
            self.services.reply_service.add_text(
                'まだ対戦結果がありません。')
            return
        current = self.get_current()
        result_ids = current.result_ids.split(',')
        self.services.results_service.drop_by_id(result_ids[i-1])
        result_ids.pop(i-1)
        current.result_ids = ','.join(result_ids)
        self.services.app_service.db.session.commit()

    def count_results(self):
        room_id = self.services.app_service.req_room_id
        match = self.services.app_service.db.session\
            .query(Matches).filter(and_(
                Matches.room_id == room_id,
                Matches.status == 1,
            )).first()
        if match is None:
            return 0
        ids = match.result_ids.split(',')
        if ids[0] == '':
            return 0
        else:
            return len(ids)

    def reply_sum_results(self):
        if self.count_results() == 0:
            self.services.reply_service.add_text(
                'まだ対戦結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        current = self.get_current()
        self.services.results_service.reply_all_by_ids(
            current.result_ids.split(',')
        )

    def finish(self):
        if self.count_results() == 0:
            self.services.reply_service.add_text(
                'まだ対戦結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        current = self.get_current()
        self.services.results_service.reply_sum_and_money_by_ids(
            current.result_ids.split(',')
        )
        self.archive()

    def archive(self):
        match = self.services.matches_service.get_current()
        match.status = 2
        self.services.app_service.db.session.commit()

    def reply(self):
        room_id = self.services.app_service.req_room_id
        matches = self.services.app_service.db.session\
            .query(Matches).filter(and_(
                Matches.room_id == room_id,
                Matches.status == 2
            )).order_by(Matches.id)\
            .all()
        if len(matches) == 0:
            self.services.reply_service.add_text(
                'まだ対戦結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        for match in matches:
            self.services.results_service.reply_sum_and_money_by_ids(
                match.result_ids.split(','),
                is_rep_sum=False,
                date=match.created_at.strftime('%Y-%m-%d')+'\n'
            )

    def drop_current(self):
        match = self.get_current()
        match.status = 0
        self.services.app_service.db.session.commit()
