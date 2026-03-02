"""user"""

import logging
import time
from functools import lru_cache

from domain_model.entities.user import User, UserMode
from messaging_api_setting import line_bot_api
from repositories import user_repository

from .interfaces.i_user_service import IUserService

logger = logging.getLogger(__name__)

_PROFILE_CACHE_TTL = 3600  # 1時間


@lru_cache(maxsize=256)
def _cached_get_profile_name(line_user_id: str, _hour_bucket: int = 0) -> str:
    """LINE API からプロフィール名を取得してキャッシュする（1時間ごとにローテート）""" # noqa: RUF002
    profile = line_bot_api.get_profile(line_user_id)
    return profile.display_name


class UserService(IUserService):
    def find_or_create_by_profile(
        self,
        profile,
    ) -> User:
        new_user = User(
            line_user_name=profile.display_name,
            line_user_id=profile.user_id,
            mode=UserMode.wait.value,
            jantama_name=None,
        )
        return user_repository.find_or_create(new_user)

    def get_name_by_line_user_id(
        self,
        line_user_id: str,
    ) -> str:
        """LINE Bot API から名前の取得を試みる(キャッシュあり)

        -> 失敗したら DB から名前の取得を試みる
        -> 失敗したら None を返す
        """
        try:
            hour_bucket = int(time.time() // _PROFILE_CACHE_TTL)
            return _cached_get_profile_name(line_user_id, hour_bucket)

        except Exception:
            target = user_repository.find(
                query={"line_user_id": line_user_id},
            )

            if len(target) == 0:
                logger.warning("user(%s) is not found", line_user_id)
                return None

            return target[0].line_user_name

    def get_line_user_id_by_name(
        self,
        line_user_name: str,
    ) -> str:
        users = user_repository.find({"line_user_name": line_user_name})

        if len(users) == 0:
            logger.warning("user_name:%s is not found", line_user_name)
            return None

        if len(users) > 1:
            logger.warning("user_name:%s is duplicated", line_user_name)
            return None

        return users[0].line_user_id

    def chmod(
        self,
        line_user_id: str,
        mode: UserMode,
    ) -> None:
        if not isinstance(mode, UserMode):
            raise ValueError(
                f"予期しないモード変更リクエストを受け取りました。'{mode}'",
            )

        user_repository.update(
            query={
                "line_user_id": line_user_id,
            },
            new_values={"mode": mode.value},
        )

        logger.info("chmod: %s: %s", line_user_id, mode.value)

    def get_mode(self, line_user_id: str) -> UserMode:
        target = user_repository.find(query={"line_user_id": line_user_id})

        if len(target) == 0:
            return None

        return target[0].mode

    def find_one_by_line_user_id(self, line_user_id: str) -> User:
        target = user_repository.find(query={"line_user_id": line_user_id})

        if len(target) == 0:
            return None

        return target[0]
