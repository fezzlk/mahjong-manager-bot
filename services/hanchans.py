"""hanchans"""

import json
from models import Hanchans
from sqlalchemy import and_, desc


class HanchansService:
    """Hanchans service"""

    def __init__(self, services):
        self.services = services

    def add(self, raw_scores={}):
        """add"""

        room_id = self.services.app_service.req_room_id
        current_match = self.services.matches_service.get_or_add_current()
        hanchan = Hanchans(
            room_id=room_id,
            match_id=current_match.id,
            raw_scores=raw_scores,
        )
        self.services.app_service.db.session.add(hanchan)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'create: room_id={room_id}')

    def delete_by_id(self, target_id):
        room_id = self.services.app_service.req_room_id
        target = self.services.app_service.db.session\
            .query(Hanchans).filter(and_(
                Hanchans.room_id == room_id,
                Hanchans.id == target_id,
            )).first()
        target.status = 0
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_id} room_id={room_id}')
        self.services.reply_service.add_message(f'id={target_id}の結果を削除しました。')

    def reply_current_hanchan(self):
        hanchan = self.get_current()
        converted_scores = json.loads(hanchan.converted_scores)
        sum_hanchans = self.services.matches_service.get_sum_hanchans()
        self.services.reply_service.add_message(f'一半荘お疲れ様でした。結果を表示します。')
        self.services.reply_service.add_message(
            '\n'.join([
                f'{self.services.user_service.get_name_by_user_id(r[0])}: {"+" if r[1] > 0 else ""}{r[1]} ({"+" if sum_hanchans[r[0]] > 0 else ""}{sum_hanchans[r[0]]})'
                for r in sorted(converted_scores.items(), key=lambda x:x[1], reverse=True)
            ])
        )
        self.services.reply_service.add_message(
            self.services.message_service.get_hanchan_message())

    def get_sum_hanchan_by_ids(self, ids):
        hanchans = self.services.app_service.db.session\
            .query(Hanchans).filter(
                Hanchans.id.in_([int(s) for s in ids]),
            )\
            .order_by(Hanchans.id)\
            .all()
        sum_hanchans = {}
        for r in hanchans:
            converted_scores = json.loads(r.converted_scores)
            for user_id, converted_score in converted_scores.items():
                if not user_id in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0
                sum_hanchans[user_id] += converted_score
        return sum_hanchans

    def reply_by_ids(self, ids, date):
        hanchans = self.services.app_service.db.session\
            .query(Hanchans).filter(
                Hanchans.id.in_([int(s) for s in ids]),
            )\
            .order_by(Hanchans.id)\
            .all()
        hanchans_list = []
        sum_hanchans = {}
        for i in range(len(ids)):
            converted_scores = json.loads(hanchans[i].converted_scores)
            hanchans_list.append(
                f'第{i+1}回\n' + '\n'.join(
                    [f'{self.services.user_service.get_name_by_user_id(r[0])}: {"+" if r[1] > 0 else ""}{r[1]}' for r in sorted(converted_scores.items(), key=lambda x:x[1], reverse=True)]
                )
            )
            for user_id, converted_score in converted_scores.items():
                if not user_id in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0
                sum_hanchans[user_id] += converted_score
        self.services.reply_service.add_message('\n\n'.join(hanchans_list))
        self.services.reply_service.add_message(
            '総計\n' + date + '\n'.join(
                [f'{self.services.user_service.get_name_by_user_id(r[0])}: {"+" if r[1] > 0 else ""}{r[1]}' for r in sorted(sum_hanchans.items(), key=lambda x:x[1], reverse=True)]
            )
        )

    def reply_sum_and_money_by_ids(self, ids, match_id, is_required_sum=True, date=''):
        hanchans = self.services.app_service.db.session\
            .query(Hanchans).filter(
                Hanchans.id.in_([int(s) for s in ids]),
            ).all()
        sum_hanchans = {}
        for i in range(len(ids)):
            converted_scores = json.loads(hanchans[i].converted_scores)
            for user_id, converted_score in converted_scores.items():
                if not user_id in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0
                sum_hanchans[user_id] += converted_score
        if is_required_sum:
            self.services.reply_service.add_message(
                '\n'.join([f'{self.services.user_service.get_name_by_user_id(user_id)}: {converted_score}' for user_id, converted_score in sum_hanchans.items()]))
        key = 'レート'
        self.services.reply_service.add_message('対戦ID: ' + str(match_id) + '\n' + date + '\n'.join(
            [f'{self.services.user_service.get_name_by_user_id(user_id)}: {converted_score * int(self.services.config_service.get_by_key(key)[1]) * 10}円 ({"+" if converted_score > 0 else ""}{converted_score})'
             for user_id, converted_score in sum_hanchans.items()]))

    def get_current(self, room_id=None):
        if room_id is None:
            room_id = self.services.app_service.req_room_id
        return self.services.app_service.db.session\
            .query(Hanchans).filter(and_(
                Hanchans.room_id == room_id,
                Hanchans.status == 1,
            ))\
            .order_by(desc(Hanchans.id))\
            .first()

    def add_raw_score(self, user_id, raw_score):
        hanchan = self.get_current()
        raw_scores = json.loads(hanchan.raw_scores)
        raw_scores[user_id] = raw_score
        hanchan.raw_scores = json.dumps(raw_scores)
        self.services.app_service.db.session.commit()
        return raw_scores

    def drop_raw_score(self, user_id):
        hanchan = self.get_current()
        raw_scores = json.loads(hanchan.raw_scores)
        if user_id in raw_scores.keys():
            raw_scores.pop(user_id)
        hanchan.raw_scores = json.dumps(raw_scores)
        self.services.app_service.db.session.commit()
        return raw_scores

    def reset_raw_scores(self):
        hanchan = self.get_current()
        hanchan.raw_scores = json.dumps({})
        self.services.app_service.db.session.commit()

    def update_hanchan(self, calculated_hanchan):
        hanchan = self.get_current()
        hanchan.converted_scores = json.dumps(calculated_hanchan)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'update hanchan: id={hanchan.id}')

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
                .query(Hanchans)\
                .order_by(Hanchans.id)\
                .all()
        else:
            if type(target_ids) != list:
                target_ids = [target_ids]
            targets = self.services.app_service.db.session\
                .query(Hanchans).filter(Hanchans.id.in_(target_ids))\
                .order_by(Hanchans.id).all()
        for hanchan in targets:
            if hanchan.raw_scores is not None:
                hanchan.raw_scores = json.loads(hanchan.raw_scores)
            if hanchan.converted_scores is not None:
                hanchan.converted_scores = json.loads(hanchan.converted_scores)
        return targets

    def delete(self, target_ids):
        if type(target_ids) != list:
            target_ids = [target_ids]
        targets = self.services.app_service.db.session\
            .query(Hanchans).filter(
                Hanchans.id.in_(target_ids),
            ).all()
        for target in targets:
            self.services.matches_service.remove_hanchan_id(
                target.match_id, target.id)
            self.services.app_service.db.session.delete(target)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_ids}')

    def migrate(self):
        targets = self.services.app_service.db.session.query(Hanchans).all()
        for t in targets:
            raw_scores = json.loads(t.raw_scores)
            new_raw_scores = {}
            for k, v in raw_scores.items():
                user_id = self.services.user_service.get_user_id_by_name(k)
                new_raw_scores[user_id] = v
            t.raw_scores = json.dumps(new_raw_scores)
            if t.converted_scores is not None:
                converted_scores = json.loads(t.converted_scores)
                new_converted_scores = {}
                for k, v in converted_scores.items():
                    user_id = self.services.user_service.get_user_id_by_name(k)
                    new_converted_scores[user_id] = v
                t.converted_scores = json.dumps(new_converted_scores)
        self.services.app_service.db.session.commit()
