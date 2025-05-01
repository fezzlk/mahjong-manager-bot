from typing import Dict

import requests

import env_var
from ApplicationService import (
    reply_service,
    request_info_service,
)
from repositories import user_repository


class JwtResponse:
    access_token: str

    def __init__(
        self,
        res_json: Dict[str, str],
    ):
        self.access_token = ""
        if "access_token" in res_json:
            self.access_token = res_json["access_token"]


class ReplyTokenUseCase:
    def execute(self) -> None:
        line_user_id = request_info_service.req_line_user_id
        users = user_repository.find(
            query={"line_user_id": line_user_id},
        )
        if len(users) == 0:
            reply_service.add_message(
                "ユーザが登録されていません。友達追加し直してください。",
            )
            return

        response = requests.post(
            env_var.SERVER_URL + env_var.JWT_AUTH_PATH,
            json={
                "_id": str(users[0]._id),
                "line_user_id": line_user_id,
            },
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        jwt_res = JwtResponse(response.json())
        reply_service.add_message(
            "JWT " + jwt_res.access_token,
        )
