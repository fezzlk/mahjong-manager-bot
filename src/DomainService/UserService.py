"""user"""

from linebot.models.responses import Profile
from .interfaces.IUserService import IUserService
from repositories import session_scope, user_repository
from messaging_api_setting import line_bot_api
from DomainModel.entities.User import User, UserMode


class UserService(IUserService):

    def find_or_create_by_profile(
        self,
        profile: Profile,
    ) -> User:
        with session_scope() as session:
            target = user_repository.find_one_by_line_user_id(
                session,
                profile.user_id,
            )

        if target is not None:
            return target

        with session_scope() as session:
            new_user = User(
                line_user_name=profile.display_name,
                line_user_id=profile.user_id,
                mode=UserMode.wait.value,
                jantama_name=None,
            )
            user_repository.create(
                session,
                new_user,
            )

            print(
                f'create: {new_user.line_user_id} {new_user.line_user_name}'
            )

            return new_user

    def get_name_by_line_user_id(
        self,
        line_user_id: str,
    ) -> str:
        """
            LINE Bot API から名前の取得を試みる
            -> 失敗したら DB から名前の取得を試みる
            -> 失敗したら LINE User ID を返す
        """
        try:
            profile = line_bot_api.get_profile(
                line_user_id,
            )

            return profile.display_name

        except Exception:
            with session_scope() as session:
                target = user_repository.find_one_by_line_user_id(
                    session,
                    line_user_id,
                )

                if target is None:
                    print(f'user({line_user_id}) is not found')
                    return line_user_id

                return target.line_user_name

    def get_line_user_id_by_name(
        self,
        line_user_name: str,
    ) -> str:
        with session_scope() as session:
            users = user_repository.find_by_name(session, line_user_name)

            if len(users) == 0:
                print(f'user({line_user_name}) is not found')
                raise ValueError(f'user({line_user_name}) is not found')

            if len(users) > 1:
                print(f'"{line_user_name}" は複数存在しているため名前からLINE IDを一意に取得できません。')
                raise ValueError(
                    f'"{line_user_name}" は複数存在しているため名前からLINE IDを一意に取得できません。')

            return users[0].line_user_id

    def chmod(
        self,
        line_user_id: str,
        mode: UserMode,
    ) -> User:
        if mode not in UserMode:
            raise ValueError(f'予期しないモード変更リクエストを受け取りました。\'{mode.value}\'')

        with session_scope() as session:
            user = user_repository.update_one_mode_by_line_user_id(
                session=session,
                line_user_id=line_user_id,
                mode=mode.value,
            )

            print(f'chmod: {line_user_id}: {mode.value}')

            return user

    def get_mode(self, line_user_id: str) -> UserMode:
        with session_scope() as session:
            target = user_repository.find_one_by_line_user_id(
                session, line_user_id)

            if target is None:
                print(f'user is not found: {line_user_id}')
                raise ValueError('ユーザーが登録されていません。友達登録をし直してください。')

            return target.mode
