from typing import List
from services import (
    user_service,
)
from domains.User import User


class GetUsersForWebUseCase:

    def execute(self) -> List[User]:
        user_service.get()
