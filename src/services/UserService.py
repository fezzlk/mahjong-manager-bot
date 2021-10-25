"""user"""

from typing import List
from linebot.models.responses import Profile
from .interfaces.IUserService import IUserService
from repositories import session_scope, user_repository
from messaging_api_setting import line_bot_api
from domains.User import User, UserMode


class UserService(IUserService):

    def delete_one_by_line_user_id(self, user_id: str) -> None:
        with session_scope() as session:
            user_repository.delete_one_by_line_user_id(session, user_id)

            print(f'delete: {user_id}')

    def find_or_create_by_profile(
        self,
        profile: Profile,
    ) -> User:
        with session_scope() as session:
            target = user_repository.find_one_by_line_user_id(
                session,
                profile.user_id,
            )

        if target is None:
            target = self.create(profile.display_name, profile.user_id)

        return target

    def create(
        self,
        name: str,
        user_id: str,
    ) -> User:
        with session_scope() as session:
            new_user = User(
                name=name,
                line_user_id=user_id,
                zoom_url=None,
                mode=UserMode.wait,
                jantama_name=None,
            )
            user_repository.create(
                session,
                new_user,
            )

            print(f'create: {new_user.line_user_id} {new_user.name}')

            return new_user

    def delete(
        self,
        ids: List[int],
    ) -> None:
        with session_scope() as session:
            user_repository.delete_by_ids(session, ids)

        print(f'delete: id={ids}')

    def get(
        self,
        ids: List[int] = None,
    ) -> List[User]:
        with session_scope() as session:
            if ids is None:
                return user_repository.find_all(session)

            return user_repository.find_by_ids(session, ids)

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
                else:
                    return target.name

    def get_line_user_id_by_name(
        self,
        name: str,
    ) -> str:
        with session_scope() as session:
            target = user_repository.find_one_by_name(session, name)

            if target is None:
                print(f'user({name}) is not found')
                return name

            return target.line_user_id

    def chmod(
        self,
        line_user_id: str,
        mode: UserMode,
    ) -> User:
        if mode not in UserMode:
            raise BaseException(f'予期しないモード変更リクエストを受け取りました。\'{mode}\'')

        with session_scope() as session:
            user = user_repository.update_one_mode_by_line_user_id(
                session=session,
                line_user_id=line_user_id,
                mode=mode,
            )

            print(f'chmod: {line_user_id}: {mode.value}')

            return user

    def get_mode(self, user_id: str) -> UserMode:
        with session_scope() as session:
            target = user_repository.find_one_by_line_user_id(session, user_id)

            if target is None:
                print(f'user is not found: {user_id}')
                raise Exception('ユーザーが登録されていません。友達登録をし直してください。')

            return target.mode

    def set_zoom_url(
        self,
        line_user_id: str,
        zoom_url: str,
    ) -> User:
        with session_scope() as session:
            user = user_repository.update_one_zoom_url_by_line_user_id(
                session=session,
                line_user_id=line_user_id,
                zoom_url=zoom_url,
            )

        print(f'set_user_url: {user.zoom_url} to {line_user_id}')
        return user

    def get_zoom_url(self, line_user_id: str) -> str:
        with session_scope() as session:
            target = user_repository.find_one_by_line_user_id(session, line_user_id)

            if target is None:
                print(f'user_services: user "{line_user_id}" is not found')
                raise Exception('ユーザーが登録されていません。友達登録をし直してください。')

            if target.zoom_url is None:
                print(
                    f'user_services: zoom id of user "{line_user_id}" is None')
                return None

            return target.zoom_url
