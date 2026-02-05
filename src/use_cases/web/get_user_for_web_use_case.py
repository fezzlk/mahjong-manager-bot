from typing import Optional

from domain_model.entities.user import User
from repositories import user_repository

from .web_utils import to_object_id


class GetUserForWebUseCase:

    def execute(self, _id) -> Optional[User]:
        records = user_repository.find({"_id": to_object_id(_id)})
        return records[0] if len(records) > 0 else None
