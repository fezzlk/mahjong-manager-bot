"""シナリオテスト共通ヘルパー関数"""
from application_service import request_info_service


def set_group_request(group_id: str, user_id: str) -> None:
    """グループチャットからのリクエスト情報をセットアップする"""
    request_info_service.req_line_group_id = group_id
    request_info_service.req_line_user_id = user_id
    request_info_service.mention_line_ids = []
    request_info_service.message = None


def set_personal_request(user_id: str, message: str = "") -> None:
    """個人チャットからのリクエスト情報をセットアップする"""
    request_info_service.req_line_group_id = None
    request_info_service.req_line_user_id = user_id
    request_info_service.mention_line_ids = []
    request_info_service.message = message
    request_info_service.parse_message()
