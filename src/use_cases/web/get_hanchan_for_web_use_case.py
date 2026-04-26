from typing import Optional

from domain_model.entities.hanchan import Hanchan
from repositories import hanchan_repository

from .web_utils import find_one_by_id


class GetHanchanForWebUseCase:

    def execute(self, _id) -> Optional[Hanchan]:
        return find_one_by_id(hanchan_repository, _id)
