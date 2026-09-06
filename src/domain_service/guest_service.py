import logging
from typing import List

from pymongo import ASCENDING

from domain_model.entities.guest import Guest
from repositories import guest_repository

from .interfaces.i_guest_service import IGuestService

logger = logging.getLogger(__name__)


class GuestService(IGuestService):

    def register_next(self, line_group_id: str) -> Guest:
        """次のguest_numberを採番して登録する。

        削除済み(is_deleted)のゲストも含め、このグループでこれまでに
        使われた最大の番号+1を採番する。削除後に番号を再利用すると、
        将来スコア記録から番号を参照する際に別人と衝突するため、
        番号は単調増加のみとし再利用しない。
        """
        max_number = guest_repository.find_max_guest_number(line_group_id)
        next_number = (max_number or 0) + 1
        new_guest = Guest(line_group_id=line_group_id, guest_number=next_number)
        guest_repository.create(new_guest)
        logger.info("register guest: group=%s number=%d", line_group_id, next_number)
        return new_guest

    def list_by_group(self, line_group_id: str) -> List[Guest]:
        return guest_repository.find(
            {"line_group_id": line_group_id},
            sort=[("guest_number", ASCENDING)],
        )

    def remove(self, line_group_id: str, guest_number: int) -> bool:
        matched = guest_repository.update(
            {"line_group_id": line_group_id, "guest_number": guest_number},
            {"is_deleted": True},
        )
        return matched > 0
