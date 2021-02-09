"""matches"""

from models import Matches
from sqlalchemy import and_
import json


class MatchesService:
    """matches service"""

    def __init__(self, services):
        self.services = services

    def get_current(self):
        room_id = self.services.app_service.req_room_id
        return self.services.app_service.db.session\
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
            self.services.app_service.db.session.add(current)
            self.services.app_service.db.session.commit()
            f'create: room_id={room_id}'
        return current

    def add_result(self):
        """add result"""
        current_result = self.services.results_service.get_current()
        current_match = self.get_or_add_current()
        result_ids = json.loads(current_match.result_ids)
        result_ids.append(str(current_result.id))
        current_match.result_ids = json.dumps(result_ids)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'update: id={current_match.id}')

    def drop_result_by_number(self, i):
        """drop result"""

        if count_results() == 0:
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
        self.services.app_service.db.session.commit()
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

    def reply_sum_results(self):
        if self.count_results() == 0:
            self.services.reply_service.add_message(
                'まだ対戦結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        current = self.get_current()
        self.services.results_service.reply_by_ids(
            json.loads(current.result_ids)
        )

    def finish(self):
        if self.count_results() == 0:
            self.services.reply_service.add_message(
                'まだ対戦結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        current = self.get_current()
        self.services.results_service.reply_sum_and_money_by_ids(
            json.loads(current.result_ids)
        )
        self.archive()

    def archive(self):
        current = self.get_current()
        match.status = 2
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'archive: id={match.id}')

    def disable(self):
        match = self.get_current()
        if match is None:
            return
        match.status = 0
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'disable: id={match.id}')

    def reply(self):
        room_id = self.services.app_service.req_room_id
        matches = self.services.app_service.db.session\
            .query(Matches).filter(and_(
                Matches.status == 2
            )).order_by(Matches.id)\
            .all()
        if len(matches) == 0:
            self.services.reply_service.add_message(
                'まだ対戦結果がありません。'
            )
            return
        for match in matches:
            self.services.results_service.reply_sum_and_money_by_ids(
                json.loads(match.result_ids),
                is_required_sum=False,
                date=match.created_at.strftime('%Y-%m-%d')+'\n'
            )

    def get(self, target_ids=None):
        if target_ids is None:
            return self.services.app_service.db.session\
                .query(Matches)\
                .order_by(Matches.id)\
                .all()
        if type(target_ids) != list:
            target_ids = [target_ids]
        return self.services.app_service.db.session\
            .query(Matches).filter(Matches.id.in_(target_ids))\
            .order_by(Matches.id).all()

    def remove_result_id(self, match_id, result_id):
        match = self.services.app_service.db.session\
            .query(Matches).filter(
                Matches.id == match_id
            ).first()
        result_ids = json.loads(match.result_ids)
        if result_id in result_ids:
            result_ids.remove(result_id)
        match.result_ids = json.dumps(result_ids)
        self.services.app_service.db.session.commit()

    def delete(self, target_ids):
        if type(target_ids) != 'list':
            target_ids = [target_ids]
        targets = self.services.app_service.db.session\
            .query(Matches).filter(
                Matches.id.in_(target_ids),
            ).all()
        for target in targets:
            self.services.results_service.delete(
                json.loads(target.result_ids)
            )
            self.services.app_service.db.session.delete(target)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_ids}')
