from typing import Dict

from ApplicationService import (
    reply_service,
    request_info_service,
)
import requests
from repositories import user_repository, session_scope


class JwtResponse:
    access_token: str

    def __init__(
        self,
        res_json: Dict[str, str],
    ):
        self.access_token = ''
        if 'access_token' in res_json:
            self.access_token = res_json['access_token']


class ReplyTokenUseCase:

    def execute(self) -> None:
        line_user_id = request_info_service.req_line_user_id
        with session_scope() as session:
            user = user_repository.find_one_by_line_user_id(
                session, line_user_id)
        response = requests.post(
            'http://localhost:5000/auth',
            json={
                '_id': user._id,
                'line_user_id': line_user_id,
            },
            headers={'Content-Type': 'application/json'},
        )
        jwt_res = JwtResponse(response.json())
        reply_service.add_message(
            'JWT ' + jwt_res.access_token
        )
