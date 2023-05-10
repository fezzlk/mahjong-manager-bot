import env_var
from flask import (
    url_for,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import (
    web_user_repository, session_scope
)


class RequestLinkLineWebUseCase():
    def execute(self) -> None:
        args = request_info_service.message.split()

        if len(args) != 2:
            reply_service.add_message(
                'Web アカウントと紐付けするには "アカウント連携 [メールアドレス]" と送ってください。')
            return

        email = args[1]
        with session_scope() as session:
            web_user = web_user_repository.find_one_by_email(
                session=session, email=email
            )

            if web_user is None:
                reply_service.add_message(
                    f'{email} は登録されていません。一度ブラウザでログインしてください。')
                reply_service.add_message(
                    f'{env_var.SERVER_URL}{url_for("line_blueprint.view_approve_link_line_user")}?openExternalBrowser=1'
                )
                return

            if web_user.is_approved_line_user:
                reply_service.add_message(
                    f'{email} はすでに LINE アカウントと紐付けされています。')
                reply_service.add_message(
                    f'{env_var.SERVER_URL}{url_for("line_blueprint.view_approve_link_line_user")}?openExternalBrowser=1'
                )
                return

            result = web_user_repository.update_linked_line_user_id(
                session=session,
                _id=web_user._id,
                line_user_id=request_info_service.req_line_user_id,
            )

            if result == 0:
                reply_service.add_message('アカウント連携リクエストに失敗しました。')
                return

            reply_service.add_message(
                'アカウント連携リクエストを送信しました。ブラウザでログインし、承認してください。')
            reply_service.add_message(
                f'{env_var.SERVER_URL}{url_for("line_blueprint.view_approve_link_line_user")}?openExternalBrowser=1'
            )
