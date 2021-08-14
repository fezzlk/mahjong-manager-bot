"""hanchans"""

import json
from repositories import session_scope
from repositories.hanchans import HanchansRepository

STATUS_LIST = ['disabled', 'active', 'archived']


class HanchansService:
    """Hanchans service"""

    def __init__(self, services):
        self.services = services

    def add(self, raw_scores={}):
        """add"""

        room_id = self.services.app_service.req_room_id
        current_match = self.services.matches_service.get_or_add_current()

        with session_scope() as session:
            HanchansRepository.create(
                session,
                room_id,
                current_match.id,
                raw_scores
            )

        self.services.app_service.logger.info(f'create: room_id={room_id}')

    def delete_by_id(self, target_id):
        """disabled target hanchan"""
        room_id = self.services.app_service.req_room_id
        with session_scope() as session:
            target = HanchansRepository.find_by_id_and_room_id(
                session,
                target_id,
                room_id
            )

            target.status = 0
            self.services.app_service.logger.info(
                f'delete: id={target_id} room_id={room_id}'
            )
            self.services.reply_service.add_message(
                f'id={target_id}の結果を削除しました。'
            )

    def reply_current_hanchan(self):
        hanchan = self.get_current()
        converted_scores = json.loads(hanchan.converted_scores)
        sum_hanchans = self.services.matches_service.get_sum_hanchans()
        self.services.reply_service.add_message(
            '一半荘お疲れ様でした。結果を表示します。'
        )
        self.services.reply_service.add_message(
            '\n'.join([
                f'{self.services.user_service.get_name_by_user_id(r[0])}: \
                {"+" if r[1] > 0 else ""}{r[1]} \
                ({"+" if sum_hanchans[r[0]] > 0 else ""}{sum_hanchans[r[0]]})'
                for r in sorted(
                    converted_scores.items(),
                    key=lambda x:x[1],
                    reverse=True
                )
            ])
        )

        self.services.reply_service.add_message(
            self.services.message_service.get_hanchan_message()
        )

    def get_sum_hanchan_by_ids(self, ids):
        with session_scope() as session:
            hanchans = HanchansRepository.find_by_ids(session, ids)

            sum_hanchans = {}
            for r in hanchans:
                converted_scores = json.loads(r.converted_scores)
                for user_id, converted_score in converted_scores.items():
                    if not user_id in sum_hanchans.keys():
                        sum_hanchans[user_id] = 0
                    sum_hanchans[user_id] += converted_score
            return sum_hanchans

    def reply_by_ids(self, ids, date):
        with session_scope() as session:
            hanchans = HanchansRepository.find_by_ids(session, ids)

        hanchans_list = []
        sum_hanchans = {}

        for i in range(len(ids)):
            converted_scores = json.loads(hanchans[i].converted_scores)
            hanchans_list.append(
                f'第{i+1}回\n' + '\n'.join([
                    f'{self.services.user_service.get_name_by_user_id(r[0])}: \
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

        self.services.reply_service.add_message('\n\n'.join(hanchans_list))
        self.services.reply_service.add_message(
            '総計\n' + date + '\n'.join([
                f'{self.services.user_service.get_name_by_user_id(r[0])}: \
                    {"+" if r[1] > 0 else ""}{r[1]}'
                for r in sorted(
                    sum_hanchans.items(),
                    key=lambda x:x[1],
                    reverse=True
                )
            ])
        )

    def reply_sum_and_money_by_ids(
        self,
        ids,
        match_id,
        is_required_sum=True,
        date=''
    ):
        with session_scope as session:
            hanchans = HanchansRepository.find_by_ids(session, ids)

            sum_hanchans = {}
            for i in range(len(ids)):
                converted_scores = json.loads(hanchans[i].converted_scores)

                for user_id, converted_score in converted_scores.items():
                    if user_id not in sum_hanchans.keys():
                        sum_hanchans[user_id] = 0
                    sum_hanchans[user_id] += converted_score

            if is_required_sum:
                self.services.reply_service.add_message(
                    '\n'.join([
                        f'{self.services.user_service.get_name_by_user_id(user_id)}: \
                            {converted_score}'
                        for user_id, converted_score in sum_hanchans.items()
                    ])
                )

            key = 'レート'
            self.services.reply_service.add_message(
                '対戦ID: ' + str(match_id) + '\n' + date + '\n'.join([
                    f'{self.services.user_service.get_name_by_user_id(user_id)}: \
                    {converted_score * int(self.services.config_service.get_by_key(key)[1]) * 10}円 \
                    ({"+" if converted_score > 0 else ""}{converted_score})'
                    for user_id, converted_score in sum_hanchans.items()
                ])
            )

    def get_current(self, room_id=None):
        if room_id is None:
            room_id = self.services.app_service.req_room_id

        with session_scope as session:
            return HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

    def add_raw_score(self, user_id, raw_score):
        room_id = self.services.app_service.req_room_id

        with session_scope as session:
            hanchan = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            raw_scores = json.loads(hanchan.raw_scores)
            raw_scores[user_id] = raw_score
            hanchan.raw_scores = json.dumps(raw_scores)
            return raw_scores

    def drop_raw_score(self, user_id):
        room_id = self.services.app_service.req_room_id

        with session_scope as session:
            hanchan = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            raw_scores = json.loads(hanchan.raw_scores)
            if user_id in raw_scores.keys():
                raw_scores.pop(user_id)

            hanchan.raw_scores = json.dumps(raw_scores)
            return raw_scores

    def reset_raw_scores(self):
        room_id = self.services.app_service.req_room_id

        with session_scope as session:
            hanchan = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            hanchan.raw_scores = json.dumps({})

    def update_hanchan(self, calculated_hanchan):
        room_id = self.services.app_service.req_room_id

        with session_scope as session:
            hanchan = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            hanchan.converted_scores = json.dumps(calculated_hanchan)
            self.services.app_service.logger.info(
                f'update hanchan: id={hanchan.id}'
            )

    def change_status(self, status):
        room_id = self.services.app_service.req_room_id
        with session_scope as session:
            current = HanchansRepository.find_by_room_id_and_status(
                session,
                room_id,
                1
            )

            if current is None:
                return
            current.status = status
            self.services.app_service.db.session.commit()
            self.services.app_service.logger.info(
                f'{STATUS_LIST[status]}: id={current.id}'
            )

    def archive(self):
        self.change_status(2)

    def disable(self):
        self.change_status(0)

    def get(self, ids=None):
        with session_scope as session:
            if ids is None:
                targets = HanchansRepository.find_all(session)
            else:
                targets = HanchansRepository.find_by_ids(session, ids)

            for hanchan in targets:
                if hanchan.raw_scores is not None:
                    hanchan.raw_scores = json.loads(hanchan.raw_scores)

                if hanchan.converted_scores is not None:
                    hanchan.converted_scores = json.loads(
                        hanchan.converted_scores
                    )

            return targets

    def delete(self, ids):
        with session_scope as session:
            targets = HanchansRepository.find_by_ids(session, ids)

            for target in targets:
                self.services.matches_service.remove_hanchan_id(
                    target.match_id, target.id)
                session.delete(target)

            self.services.app_service.logger.info(f'delete: id={ids}')

    def migrate(self):
        with session_scope as session:
            targets = HanchansRepository.find_all(session)

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
