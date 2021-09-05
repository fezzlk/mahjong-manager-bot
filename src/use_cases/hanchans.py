"""hanchans"""

import json
from services import (
    app_service,
    matches_service,
    reply_service,
    user_service,
    message_service,
    config_service,
    hanchans_service,
)
from use_cases import calculate_use_cases, user_use_cases

STATUS_LIST = ['disabled', 'active', 'archived']


class HanchansUseCases:
    """Hanchans use cases"""

    def add(self, raw_scores={}):
        """add"""

        room_id = app_service.req_room_id
        current_match = matches_service.get_or_add_current()
        hanchans_service.add(raw_scores, room_id, current_match)

    def delete_by_id(self, target_id):
        room_id = app_service.req_room_id
        hanchans_service.delete_by_id(room_id, target_id)
        reply_service.add_message(
            f'id={target_id}の結果を削除しました。'
        )

    def get_sum_hanchan_by_ids(self, ids):
        hanchans = hanchans_service.find_by_ids(ids)
        sum_hanchans = {}
        for r in hanchans:
            converted_scores = json.loads(r.converted_scores)
            for user_id, converted_score in converted_scores.items():
                if user_id not in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0
                sum_hanchans[user_id] += converted_score
        return sum_hanchans

    def reply_by_ids(self, ids, date):
        hanchans = hanchans_service.find_by_ids(ids)

        hanchans_list = []
        sum_hanchans = {}

        for i in range(len(ids)):
            converted_scores = json.loads(hanchans[i].converted_scores)
            hanchans_list.append(
                f'第{i+1}回\n' + '\n'.join([
                    f'{user_service.get_name_by_user_id(r[0])}: \
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

        reply_service.add_message('\n\n'.join(hanchans_list))
        reply_service.add_message(
            '総計\n' + date + '\n'.join([
                f'{user_service.get_name_by_user_id(r[0])}: \
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
        hanchans = hanchans_service.find_by_ids(ids)

        sum_hanchans = {}
        for i in range(len(ids)):
            converted_scores = json.loads(hanchans[i].converted_scores)

            for user_id, converted_score in converted_scores.items():
                if user_id not in sum_hanchans.keys():
                    sum_hanchans[user_id] = 0
                sum_hanchans[user_id] += converted_score

        if is_required_sum:
            reply_service.add_message(
                '\n'.join([
                    f'{user_service.get_name_by_user_id(user_id)}: \
                        {converted_score}'
                    for user_id, converted_score in sum_hanchans.items()
                ])
            )

        key = 'レート'
        room_id = app_service.req_room_id
        reply_service.add_message(
            '対戦ID: ' + str(match_id) + '\n' + date + '\n'.join([
                f'{user_service.get_name_by_user_id(user_id)}: \
                {converted_score * int(config_service.get_by_key(room_id, key)[1]) * 10}円 \
                ({"+" if converted_score > 0 else ""}{converted_score})'
                for user_id, converted_score in sum_hanchans.items()
            ])
        )

    def add_raw_score(self, user_id, raw_score):
        room_id = app_service.req_room_id
        return hanchans_service.add_raw_score(room_id, user_id, raw_score)

    def drop_raw_score(self, user_id):
        room_id = app_service.req_room_id
        return hanchans_service.drop_raw_score(room_id, user_id)

    # clear の方がいいのでは
    def reset_raw_scores(self):
        room_id = app_service.req_room_id
        hanchans_service.reset_raw_scores(room_id)

    def get(self, ids=None):
        return hanchans_service.get(ids)

    def delete(self, ids):
        deleted_hanchans = hanchans_service.delete(ids)
        for deleted_hanchan in deleted_hanchans:
            matches_service.remove_hanchan_id(
                deleted_hanchan.match_id, deleted_hanchan.id
            )

    def migrate(self):
        targets = hanchans_service.get()

        for t in targets:
            raw_scores = json.loads(t.raw_scores)

            new_raw_scores = {}
            for k, v in raw_scores.items():
                user_id = user_service.get_user_id_by_name(k)
                new_raw_scores[user_id] = v
            t.raw_scores = json.dumps(new_raw_scores)

            if t.converted_scores is not None:
                converted_scores = json.loads(t.converted_scores)

                new_converted_scores = {}
                for k, v in converted_scores.items():
                    user_id = user_service.get_user_id_by_name(k)
                    new_converted_scores[user_id] = v

                t.converted_scores = json.dumps(new_converted_scores)
