from dummies import generate_dummy_text_message_event_from_group
from linebot.v3.messaging import TextMessage

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.match import Match, MatchStatus
from repositories import group_repository, match_repository
from use_cases.group_line.reopen_match_use_case import ReopenMatchUseCase

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"


def _setup_request(params=None):
    event = generate_dummy_text_message_event_from_group()
    event.group_id = _LINE_GROUP_ID
    request_info_service.set_req_info(event=event)
    if params:
        request_info_service.params = params


def test_execute_shows_picker_even_while_another_match_is_open():
    """複数対戦の同時openを許容するため(FEZ-66 Phase D)、他に進行中の対戦や
    simモード中でも_reopenの選択肢提示自体はブロックしない。
    """
    group_repository.create(
        Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.input.value, current_input_match_id="dummy"),
    )
    match_repository.create(
        Match(line_group_id=_LINE_GROUP_ID, status=MatchStatus.settled.value, name="settled"),
    )
    _setup_request()

    ReopenMatchUseCase().execute()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].quick_reply is not None


def test_execute_no_settled_matches():
    """精算済みの対戦が1件もなければエラーメッセージを返す。"""
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.wait.value))
    _setup_request()

    ReopenMatchUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "見つかりません" in reply_service.texts[0].text


def test_execute_shows_only_settled_matches_up_to_five():
    """openなMatchは除外し、settled最大5件のみをQuick Replyで提示する。"""
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.wait.value))
    match_repository.create(
        Match(line_group_id=_LINE_GROUP_ID, status=MatchStatus.open.value, name="open match"),
    )
    for i in range(6):
        match_repository.create(
            Match(line_group_id=_LINE_GROUP_ID, status=MatchStatus.settled.value, name=f"settled{i}"),
        )
    _setup_request()

    ReopenMatchUseCase().execute()

    assert len(reply_service.texts) == 1
    msg = reply_service.texts[0]
    assert isinstance(msg, TextMessage)
    assert msg.quick_reply is not None
    assert len(msg.quick_reply.items) == 5
    labels = {item.action.label for item in msg.quick_reply.items}
    assert "open match" not in labels


def test_confirm_reopens_target_match():
    """_reopen_confirm?to=<id> で対象Matchがopenへ戻る。

    reopenは「openな対戦のプールに戻す」だけで、グループの入力セッション状態
    (current_input_match_id/mode)には触れない(FEZ-66 Phase D)。
    """
    group_repository.create(
        Group(
            line_group_id=_LINE_GROUP_ID,
            mode=GroupMode.input.value,
            current_input_match_id="other_match",
        ),
    )
    target = match_repository.create(
        Match(
            line_group_id=_LINE_GROUP_ID,
            status=MatchStatus.settled.value,
            name="9/1",
            sum_prices={"U1": 100},
            chip_prices={"U1": 1},
            sum_prices_with_chip={"U1": 101},
        ),
    )
    _setup_request(params={"to": str(target._id)})

    ReopenMatchUseCase().confirm()

    reopened = match_repository.find({"_id": target._id})[0]
    assert reopened.status == MatchStatus.open.value
    assert reopened.sum_prices == {}
    assert reopened.chip_prices == {}
    assert reopened.sum_prices_with_chip == {}

    # 他の対戦の入力セッション状態は変化しない
    groups = group_repository.find({"line_group_id": _LINE_GROUP_ID})
    assert groups[0].current_input_match_id == "other_match"
    assert groups[0].mode == GroupMode.input.value

    assert len(reply_service.texts) == 1
    assert "再オープンしました" in reply_service.texts[0].text


def test_confirm_invalid_match_id():
    """存在しないMatchを指定した場合はエラーメッセージが返る。"""
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.wait.value))
    _setup_request(params={"to": "644c838186bbd9e20a91b785"})

    ReopenMatchUseCase().confirm()

    assert len(reply_service.texts) == 1
    assert "見つかりません" in reply_service.texts[0].text


def test_confirm_malformed_match_id():
    """不正な形式のmatch_idを指定した場合、例外を投げずエラーメッセージが返る。"""
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.wait.value))
    _setup_request(params={"to": "not-a-valid-object-id"})

    ReopenMatchUseCase().confirm()

    assert len(reply_service.texts) == 1
    assert "見つかりません" in reply_service.texts[0].text


def test_confirm_succeeds_while_another_match_is_open():
    """確定時点で他に進行中の対戦やsimモード実行中でもブロックしない
    (FEZ-66 Phase D、複数対戦の同時open許容)。
    """
    group_repository.create(
        Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.sim.value, sim_match_id="dummy"),
    )
    target = match_repository.create(
        Match(line_group_id=_LINE_GROUP_ID, status=MatchStatus.settled.value, name="9/1"),
    )
    _setup_request(params={"to": str(target._id)})

    ReopenMatchUseCase().confirm()

    reopened = match_repository.find({"_id": target._id})[0]
    assert reopened.status == MatchStatus.open.value
    assert len(reply_service.texts) == 1
    assert "再オープンしました" in reply_service.texts[0].text
