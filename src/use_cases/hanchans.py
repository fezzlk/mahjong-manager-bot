# flake8: noqa: E999
"""hanchans"""

import json
from services import (
    request_info_service,
    matches_service,
    reply_service,
    user_service,
    config_service,
    hanchan_service,
)

STATUS_LIST = ['disabled', 'active', 'archived']


class HanchansUseCases:
    """Hanchans use cases"""

    def add(self, raw_scores={}):
        """add"""

        room_id = request_info_service.req_line_room_id
        current_match = matches_service.get_or_add_current(room_id)
        hanchan_service.add(raw_scores, room_id, current_match)

    def get(self, ids=None):
        return hanchan_service.get(ids)

    def delete(self, ids):
        deleted_hanchans = hanchan_service.delete(ids)
        for deleted_hanchan in deleted_hanchans:
            matches_service.remove_hanchan_id(
                deleted_hanchan.match_id, deleted_hanchan.id
            )

    def migrate(self):
        targets = hanchan_service.get()

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
