from dummies import (
    generate_dummy_group_list,
    generate_dummy_text_message_event_from_group,
    generate_dummy_text_message_event_from_user,
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


# --- 個人DM フロー ---

def _setup_personal_request(params=None):
    event = generate_dummy_text_message_event_from_user()
    request_info_service.set_req_info(event=event)
    if params:
        request_info_service.params = params


def test_execute_personal_step1_shows_source_quick_reply():
    """個人DM: params なし → 統合元選択 QR が返る（2グループ以上必要）。"""
    group_repository.create(_SRC_GROUP)
    group_repository.create(_DST_GROUP)
    user_group_repository.create(
        UserGroup(line_user_id=_USER.line_user_id, line_group_id=_SRC_GROUP.line_group_id),
    )
    user_group_repository.create(
        UserGroup(line_user_id=_USER.line_user_id, line_group_id=_DST_GROUP.line_group_id),
    )
    _setup_personal_request()

    MigrateGroupUseCase().execute_personal()

    assert len(reply_service.texts) == 1
    msg = reply_service.texts[0]
    assert isinstance(msg, TextMessage)
    assert msg.quick_reply is not None
    assert len(msg.quick_reply.items) == 2


def test_execute_personal_step1_too_few_groups():
    """個人DM: 1グループのみ → エラーメッセージ。"""
    group_repository.create(_SRC_GROUP)
    user_group_repository.create(
        UserGroup(line_user_id=_USER.line_user_id, line_group_id=_SRC_GROUP.line_group_id),
    )
    _setup_personal_request()

    MigrateGroupUseCase().execute_personal()

    assert len(reply_service.texts) == 1
    assert "2つ以上" in reply_service.texts[0].text


def test_execute_personal_step2_shows_dest_quick_reply():
    """個人DM: src=<id> → 統合先選択 QR が返る。"""
    group_repository.create(_SRC_GROUP)
    group_repository.create(_DST_GROUP)
    user_group_repository.create(
        UserGroup(line_user_id=_USER.line_user_id, line_group_id=_SRC_GROUP.line_group_id),
    )
    user_group_repository.create(
        UserGroup(line_user_id=_USER.line_user_id, line_group_id=_DST_GROUP.line_group_id),
    )
    _setup_personal_request(params={"src": _SRC_GROUP.line_group_id})

    MigrateGroupUseCase().execute_personal()

    assert len(reply_service.texts) == 2  # "選んでください" + Quick Reply
    assert reply_service.texts[1].quick_reply is not None
    assert len(reply_service.texts[1].quick_reply.items) == 1  # DST_GROUP のみ


def test_execute_personal_step3_confirms():
    """個人DM: src=<id>&to=<id> → merged_into がセットされる。"""
    group_repository.create(_SRC_GROUP)
    group_repository.create(_DST_GROUP)
    _setup_personal_request(params={
        "src": _SRC_GROUP.line_group_id,
        "to": _DST_GROUP.line_group_id,
    })

    MigrateGroupUseCase().execute_personal()

    result = group_repository.find({"line_group_id": _SRC_GROUP.line_group_id})
    assert result[0].merged_into == _DST_GROUP.line_group_id
    assert "統合しました" in reply_service.texts[0].text
