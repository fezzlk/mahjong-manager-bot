from typing import List

from domain_model.entities.user import User
from repositories import user_repository


class GetUsersForWebUseCase:

    def execute(self) -> List[User]:
        return user_repository.find()
