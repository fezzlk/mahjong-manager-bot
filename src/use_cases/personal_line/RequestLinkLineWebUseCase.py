from flask import (
    url_for,
)

import env_var
from ApplicationService import (
    reply_service,
    request_info_service,
)
from repositories import web_user_repository


class RequestLinkLineWebUseCase:
    def execute(self) -> None:
        args = request_info_service.message.split()

        if len(args) != 2:
            reply_service.add_message(
                'Web アカウントと紐付けするには "アカウント連携 [メールアドレス]" と送ってください。')
            return

        email = args[1]
        web_users = web_user_repository.find(
            query={
                "email": email,
            },
        )

        if len(web_users) == 0:
            reply_service.add_message(
                f"{email} は登録されていません。一度ブラウザでログインしてください。")
            reply_service.add_message(
                f'{env_var.SERVER_URL}{url_for("line_blueprint.view_approve_link_line_user")}?openExternalBrowser=1',
            )
            return

        if web_users[0].is_approved_line_user:
            reply_service.add_message(
                f"{email} はすでに LINE アカウントと紐付けされています。")
            reply_service.add_message(
                f'{env_var.SERVER_URL}{url_for("line_blueprint.view_approve_link_line_user")}?openExternalBrowser=1',
            )
            return

        result = web_user_repository.update(
            query={
                "_id": web_users[0]._id,
            },
            new_values={
                "line_user_id": request_info_service.req_line_user_id,
            },
        )

        if result == 0:
            reply_service.add_message("アカウント連携リクエストに失敗しました。")
            return

        reply_service.add_message(
            "アカウント連携リクエストを送信しました。ブラウザでログインし、承認してください。")
        reply_service.add_message(
            f'{env_var.SERVER_URL}{url_for("line_blueprint.view_approve_link_line_user")}?openExternalBrowser=1',
        )
