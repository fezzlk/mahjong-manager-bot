from dummies import (
    generate_dummy_group_list,
    generate_dummy_text_message_event_from_group,
    generate_dummy_user_list,
)
from linebot.v3.messaging import TextMessage

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.user_group import UserGroup
from repositories import (
    group_repository,
    user_group_repository,
)
from use_cases.group_line.migrate_group_use_case import MigrateGroupUseCase

_DUMMY_GROUPS = generate_dummy_group_list()
_DUMMY_USERS = generate_dummy_user_list()

_SRC_GROUP = _DUMMY_GROUPS[0]   # 統合元（旧グループ）
_DST_GROUP = _DUMMY_GROUPS[1]   # 統合先（新グループ）
_USER = _DUMMY_USERS[0]


def _setup_request(group_id=None, params=None):
    event = generate_dummy_text_message_event_from_group()
    if group_id:
        event.group_id = group_id
    request_info_service.set_req_info(event=event)
    if params:
        request_info_service.params = params


def test_execute_shows_quick_reply():
    """2グループ所属時に統合先選択 Quick Reply が返る。"""
    group_repository.create(_SRC_GROUP)
    group_repository.create(_DST_GROUP)
    user_group_repository.create(
        UserGroup(line_user_id=_USER.line_user_id, line_group_id=_SRC_GROUP.line_group_id),
    )
    user_group_repository.create(
        UserGroup(line_user_id=_USER.line_user_id, line_group_id=_DST_GROUP.line_group_id),
    )
    _setup_request(group_id=_SRC_GROUP.line_group_id)

    MigrateGroupUseCase().execute()

    assert len(reply_service.texts) == 1
    msg = reply_service.texts[0]
    assert isinstance(msg, TextMessage)
    assert msg.quick_reply is not None
    assert len(msg.quick_reply.items) == 1  # DST_GROUP のみ（SRC は除外）


def test_execute_no_candidates():
    """他グループが存在しない場合はエラーメッセージが返る。"""
    group_repository.create(_SRC_GROUP)
    user_group_repository.create(
        UserGroup(line_user_id=_USER.line_user_id, line_group_id=_SRC_GROUP.line_group_id),
    )
    _setup_request(group_id=_SRC_GROUP.line_group_id)

    MigrateGroupUseCase().execute()

    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextMessage)
    assert "見つかりません" in reply_service.texts[0].text


def test_confirm_sets_merged_into():
    """_migrate_confirm?to=<id> で merged_into がセットされ確認メッセージが返る。"""
    group_repository.create(_SRC_GROUP)
    dst = group_repository.create(_DST_GROUP)
    _setup_request(
        group_id=_SRC_GROUP.line_group_id,
        params={"to": _DST_GROUP.line_group_id},
    )

    MigrateGroupUseCase().confirm()

    result = group_repository.find({"line_group_id": _SRC_GROUP.line_group_id})
    assert len(result) == 1
    assert result[0].merged_into == _DST_GROUP.line_group_id

    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextMessage)
    assert "統合しました" in reply_service.texts[0].text


def test_confirm_invalid_to():
    """存在しない統合先を指定した場合はエラーメッセージが返る。"""
    group_repository.create(_SRC_GROUP)
    _setup_request(
        group_id=_SRC_GROUP.line_group_id,
        params={"to": "G_nonexistent_group_id"},
    )

    MigrateGroupUseCase().confirm()

    assert len(reply_service.texts) == 1
    assert "存在しません" in reply_service.texts[0].text
