from typing import Optional

from domain_model.entities.user import User
from repositories import user_repository

from .web_utils import find_one_by_id


class GetUserForWebUseCase:

    def execute(self, _id) -> Optional[User]:
        return find_one_by_id(user_repository, _id)
