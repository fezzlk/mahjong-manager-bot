"""精算結果の「場代を入力」→数字送信で最終会計を表示するフロー(FEZ-234)。"""
from datetime import datetime

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.match import Match, MatchStatus
from domain_model.entities.user import User
from line_models.event import Event
from repositories import (
    group_repository,
    match_repository,
    user_repository,
)
from use_cases.group_line.exit_use_case import ExitUseCase
from use_cases.group_line.reply_apply_badai_use_case import ReplyApplyBadaiUseCase

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id=_LINE_GROUP_ID,
    message_type="text",
    text="dummy",
)


def _setup(mode=GroupMode.wait.value, status=MatchStatus.settled.value):
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=mode))
    for i, name in enumerate(["Alice", "Bob"]):
        user_repository.create(User(line_user_id=f"U_badai_{i}", line_user_name=name))
    match = match_repository.create(
        Match(
            line_group_id=_LINE_GROUP_ID,
            status=status,
            created_at=datetime(2026, 9, 1),
            sum_prices_with_chip={"U_badai_0": 1000, "U_badai_1": -1000},
        ),
    )
    request_info_service.set_req_info(event=dummy_event)
    return match


def _group():
    return group_repository.find({"line_group_id": _LINE_GROUP_ID})[0]


def test_start_enters_badai_input_mode():
    match = _setup()
    request_info_service.params = {"to": str(match._id)}

    ReplyApplyBadaiUseCase().start()

    group = _group()
    assert group.mode == GroupMode.badai_input.value
    assert group.current_input_match_id == match._id
    assert reply_service.texts[0].quick_reply.items[0].action.data == "_exit"


def test_start_rejected_while_other_input_in_progress():
    match = _setup(mode=GroupMode.input.value)
    request_info_service.params = {"to": str(match._id)}

    ReplyApplyBadaiUseCase().start()

    assert _group().mode == GroupMode.input.value
    assert "別の入力が進行中" in reply_service.texts[0].text


def test_start_rejects_unsettled_match():
    match = _setup(status=MatchStatus.open.value)
    request_info_service.params = {"to": str(match._id)}

    ReplyApplyBadaiUseCase().start()

    assert _group().mode == GroupMode.wait.value
    assert reply_service.texts[0].text == "指定された対戦が見つかりません。"


def test_input_shows_result_and_returns_to_wait():
    match = _setup()
    request_info_service.params = {"to": str(match._id)}
    ReplyApplyBadaiUseCase().start()
    reply_service.reset()

    ReplyApplyBadaiUseCase().input("2,000")

    texts = [t.text for t in reply_service.texts]
    assert texts[0] == "場代込みの最終会計を表示します。"
    assert texts[1] == "対戦開始日: 2026年09月01日\n場代: 2000pt(1000pt×2人)\nAlice: 0pt\nBob: -2000pt"
    group = _group()
    assert group.mode == GroupMode.wait.value
    assert group.current_input_match_id is None


def test_input_invalid_keeps_mode():
    match = _setup()
    request_info_service.params = {"to": str(match._id)}
    ReplyApplyBadaiUseCase().start()
    reply_service.reset()

    ReplyApplyBadaiUseCase().input("にせん")

    assert reply_service.texts[0].text == "場代は自然数で入力してください。"
    assert _group().mode == GroupMode.badai_input.value


def test_exit_cancels_badai_input():
    match = _setup()
    request_info_service.params = {"to": str(match._id)}
    ReplyApplyBadaiUseCase().start()

    ExitUseCase().execute()

    group = _group()
    assert group.mode == GroupMode.wait.value
    assert group.current_input_match_id is None
    # 精算済みの対戦には触れない
    assert match_repository.find({"_id": match._id})[0].status == MatchStatus.settled.value
