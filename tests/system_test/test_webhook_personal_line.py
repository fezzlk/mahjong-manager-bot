"""システムテスト: 個人チャット LINE Webhook 統合テスト

個人チャットのコマンドを /test_personal_line エンドポイント経由でテスト。
このエンドポイントはFLASK_ENV != "production" の場合のみ利用可能。
"""

from conftest import client  # noqa: F401

from application_service import reply_service, request_info_service, rich_menu_service
from domain_model.entities.user import User
from line_models.event import Event
from messaging_api_setting import line_bot_api
from repositories import user_repository
from use_cases.personal_line.follow_use_case import FollowUseCase
from use_cases.personal_line.unfollow_use_case import UnfollowUseCase

USER_ID = "U_system_test_personal_001_abcd"


def _make_dummy_profile(user_id: str = USER_ID):
    """LINE API get_profile のダミーレスポンス"""
    from line_models.profile import Profile  # noqa: PLC0415
    return Profile(display_name="test_display_name", user_id=user_id)


def test_follow_event_registers_user(mocker):
    """フォローイベント: FollowUseCase を直接呼び出してユーザー登録を確認"""
    mocker.patch.object(line_bot_api, "get_profile", return_value=_make_dummy_profile())
    mocker.patch.object(rich_menu_service, "create_and_link", return_value=None)

    event = Event(type="follow", source_type="user", user_id=USER_ID)
    request_info_service.set_req_info(event)

    FollowUseCase().execute()

    users = user_repository.find({"line_user_id": USER_ID})
    assert len(users) == 1
    assert users[0].line_user_id == USER_ID
    assert len(reply_service.texts) >= 1


def test_unfollow_event_after_follow(mocker):
    """フォロー解除イベント: UnfollowUseCase を直接呼び出してユーザーが削除される"""
    follow_uid = USER_ID + "_uf"
    mocker.patch.object(line_bot_api, "get_profile", return_value=_make_dummy_profile(follow_uid))
    mocker.patch.object(rich_menu_service, "create_and_link", return_value=None)

    # まずフォローしてユーザーを登録
    follow_event = Event(type="follow", source_type="user", user_id=follow_uid)
    request_info_service.set_req_info(follow_event)
    FollowUseCase().execute()

    users_before = user_repository.find({"line_user_id": follow_uid})
    assert len(users_before) == 1

    # アンフォロー
    unfollow_event = Event(type="unfollow", source_type="user", user_id=follow_uid)
    request_info_service.set_req_info(unfollow_event)
    UnfollowUseCase().execute()

    # ユーザーが削除されている (is_deleted = True または find で 0 件)
    users_after = user_repository.find({"line_user_id": follow_uid})
    assert len(users_after) == 0 or users_after[0].is_deleted is True


def test_personal_line_endpoint_help_command(client):
    """POST /test_personal_line ?text=_help → help メッセージが返る"""
    # ユーザーを事前に登録
    user_repository.create(
        User(line_user_id=USER_ID + "_help", line_user_name="test_user"),
    )
    resp = client.post(
        "/test_personal_line",
        data={"user_id": USER_ID + "_help", "text": "_help"},
    )
    assert resp.status_code == 200
    assert len(resp.data) > 0  # 何らかのレスポンスが返る


def test_personal_line_endpoint_unknown_command(client):
    """POST /test_personal_line ?text=unknown → 何らかのレスポンスが返る"""
    # ユーザーを事前に登録 (未登録だと「ユーザーが登録されていません」メッセージが返る)
    user_repository.create(
        User(line_user_id=USER_ID + "_unknown", line_user_name="test_unknown_user"),
    )
    resp = client.post(
        "/test_personal_line",
        data={"user_id": USER_ID + "_unknown", "text": "unknown_text_xyz"},
    )
    assert resp.status_code == 200
    # 未知のコマンドに対してもランダムなフォールバックメッセージが返る
