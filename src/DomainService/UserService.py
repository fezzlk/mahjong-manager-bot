"""user"""

from linebot.models.responses import Profile

from DomainModel.entities.User import User, UserMode
from messaging_api_setting import line_bot_api
from repositories import user_repository

from .interfaces.IUserService import IUserService


class UserService(IUserService):
    def find_or_create_by_profile(
        self,
        profile: Profile,
    ) -> User:
        users = user_repository.find(
            query={"line_user_id": profile.user_id},
        )

        if len(users) > 0:
            return users[0]

        new_user = User(
            line_user_name=profile.display_name,
            line_user_id=profile.user_id,
            mode=UserMode.wait.value,
            jantama_name=None,
        )
        user_repository.create(new_user)

        print(
            f"create user: {new_user.line_user_id} {new_user.line_user_name}",
        )

        return new_user

    def get_name_by_line_user_id(
        self,
        line_user_id: str,
    ) -> str:
        """LINE Bot API から名前の取得を試みる

        -> 失敗したら DB から名前の取得を試みる
        -> 失敗したら None を返す
        """
        try:
            profile = line_bot_api.get_profile(
                line_user_id,
            )

            return profile.display_name

        except Exception:
            target = user_repository.find(
                query={"line_user_id": line_user_id},
            )

            if len(target) == 0:
                print(f"user({line_user_id}) is not found")
                return None

            return target[0].line_user_name

    def get_line_user_id_by_name(
        self,
        line_user_name: str,
    ) -> str:
        users = user_repository.find({"line_user_name": line_user_name})

        if len(users) == 0:
            print(f"user_name:{line_user_name} is not found")
            return None

        if len(users) > 1:
            print(f"user_name:{line_user_name} is duplicated")
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

        print(f"chmod: {line_user_id}: {mode.value}")

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
