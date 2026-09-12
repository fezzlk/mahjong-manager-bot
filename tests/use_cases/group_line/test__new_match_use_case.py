from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from line_models.event import Event
from repositories import group_repository, match_repository
from use_cases.group_line.new_match_use_case import NewMatchUseCase

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"

_dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id=_LINE_GROUP_ID,
    message_type="text",
    text="_new_match",
)


def _setup_request():
    request_info_service.set_req_info(event=_dummy_event)


def test_execute_no_group():
    _setup_request()

    NewMatchUseCase().execute()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "グループが登録されていません。招待し直してください。"


def test_execute_blocked_while_input_mode():
    _setup_request()
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.input.value))

    NewMatchUseCase().execute()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "すでに入力モードです。"


def test_execute_shows_confirm_button():
    _setup_request()
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.wait.value))

    NewMatchUseCase().execute()

    assert len(reply_service.texts) == 0
    assert len(reply_service.buttons) == 1
    button = reply_service.buttons[0]
    assert button.template.actions[0].data == "_new_match_confirm"


def test_confirm_creates_and_enters_new_match():
    _setup_request()
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.wait.value))

    NewMatchUseCase().confirm()

    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "第1回戦お疲れ様です。各自点数を入力してください。\n(同点の場合は上家が高くなるように数点追加してください)"
    )
    groups = group_repository.find({"line_group_id": _LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.input.value
    assert groups[0].current_input_match_id is not None
    matches = match_repository.find({"line_group_id": _LINE_GROUP_ID})
    assert len(matches) == 1


def test_confirm_adds_another_match_even_when_one_is_already_open():
    """既にopenな対戦が1件あっても、_new_match_confirmは常に新規対戦を
    追加する(複数系列同時進行の核心)。
    """
    _setup_request()
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.wait.value))
    NewMatchUseCase().confirm()
    first_match_id = group_repository.find({"line_group_id": _LINE_GROUP_ID})[0].current_input_match_id

    # 1件目の入力を終えて待機状態に戻す
    group = group_repository.find({"line_group_id": _LINE_GROUP_ID})[0]
    group.mode = GroupMode.wait.value
    group_repository.update({"_id": group._id}, {"mode": GroupMode.wait.value})

    reply_service.reset()
    NewMatchUseCase().confirm()

    matches = match_repository.find({"line_group_id": _LINE_GROUP_ID})
    assert len(matches) == 2
    group = group_repository.find({"line_group_id": _LINE_GROUP_ID})[0]
    assert group.current_input_match_id != first_match_id
    open_matches = match_repository.find({"line_group_id": _LINE_GROUP_ID, "status": "open"})
    assert len(open_matches) == 2
