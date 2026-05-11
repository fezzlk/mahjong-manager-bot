"""_input コマンドと整数メッセージの並行処理（レース条件対策）テスト。

- _input 直後（5秒以内）に整数が来た場合 → auto-start input で処理される
- _input から5秒超過後に整数が来た場合 → auto-start しない
- last_command が input 以外の場合 → auto-start しない
"""
from datetime import datetime, timedelta

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.user import User, UserMode
from line_models.event import Event
from repositories import (
    group_repository,
    match_repository,
    user_repository,
)
from routing_by_text_in_group_line import routing_by_text_in_group_line

LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"
USER_ID = "U0123456789abcdefghijklmnopqrstu1"


def _make_event(text: str) -> Event:
    return Event(
        type="message",
        source_type="group",
        user_id=USER_ID,
        group_id=LINE_GROUP_ID,
        message_type="text",
        text=text,
    )


def _setup_user():
    user_repository.create(
        User(
            line_user_name="test_user",
            line_user_id=USER_ID,
            mode=UserMode.wait.value,
            _id=1,
        ),
    )


def test_auto_start_within_window():
    """_input 直後（5秒以内）に整数が送られた場合、auto-start で input になり点数が処理される。"""
    _setup_user()
    # _input が直前に実行された状態をシミュレート
    group_repository.create(
        Group(
            line_group_id=LINE_GROUP_ID,
            mode=GroupMode.wait.value,
            last_command="input",
            last_command_at=datetime.now(),  # 直前
            _id=1,
        ),
    )

    # 整数メッセージを送信
    request_info_service.set_req_info(event=_make_event("35000"))
    routing_by_text_in_group_line()

    # auto-start が発動し、input モードで点数が処理される
    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.input.value

    # match と hanchan が作成されている
    matches = match_repository.find()
    assert len(matches) >= 1


def test_no_auto_start_after_window():
    """_input から5秒超過後に整数が送られた場合、auto-start しない。"""
    _setup_user()
    group_repository.create(
        Group(
            line_group_id=LINE_GROUP_ID,
            mode=GroupMode.wait.value,
            last_command="input",
            last_command_at=datetime.now() - timedelta(seconds=10),  # 10秒前
            _id=1,
        ),
    )

    request_info_service.set_req_info(event=_make_event("35000"))
    routing_by_text_in_group_line()

    # auto-start は発動しない（wait のまま）
    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.wait.value
    # メッセージも出ない（wait モードで整数は無視される）
    assert len(reply_service.texts) == 0


def test_no_auto_start_without_last_command():
    """last_command が input 以外の場合、auto-start しない。"""
    _setup_user()
    group_repository.create(
        Group(
            line_group_id=LINE_GROUP_ID,
            mode=GroupMode.wait.value,
            last_command="exit",
            last_command_at=datetime.now(),
            _id=1,
        ),
    )

    request_info_service.set_req_info(event=_make_event("35000"))
    routing_by_text_in_group_line()

    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.wait.value


def test_no_auto_start_without_timestamp():
    """last_command_at が None の場合（旧データ）、auto-start しない。"""
    _setup_user()
    group_repository.create(
        Group(
            line_group_id=LINE_GROUP_ID,
            mode=GroupMode.wait.value,
            last_command="input",
            last_command_at=None,
            _id=1,
        ),
    )

    request_info_service.set_req_info(event=_make_event("35000"))
    routing_by_text_in_group_line()

    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.wait.value


def test_no_auto_start_for_non_numeric():
    """数値でないメッセージでは auto-start しない。"""
    _setup_user()
    group_repository.create(
        Group(
            line_group_id=LINE_GROUP_ID,
            mode=GroupMode.wait.value,
            last_command="input",
            last_command_at=datetime.now(),
            _id=1,
        ),
    )

    request_info_service.set_req_info(event=_make_event("こんにちは"))
    routing_by_text_in_group_line()

    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.wait.value
