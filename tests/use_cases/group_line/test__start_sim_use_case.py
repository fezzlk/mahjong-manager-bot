from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from line_models.event import Event
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
)
from use_cases.group_line.start_sim_use_case import StartSimUseCase

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="_sim",
)


def test_no_group():
    """グループ未登録の場合エラーメッセージを返す。"""
    request_info_service.set_req_info(event=dummy_event)
    StartSimUseCase().execute()
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "トークルームが登録されていません。招待し直してください。"


def test_already_sim_mode():
    """すでにsimモードの場合エラーメッセージを返す。"""
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.sim.value,
            _id=1,
        ),
    )
    StartSimUseCase().execute()
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "すでにシミュレーションモードです。"


def test_new_match_and_hanchan():
    """Match も hanchan もない場合、両方新規作成してsimモードになる。"""
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(
        Group(line_group_id="G0123456789abcdefghijklmnopqrstu1", _id=1),
    )
    StartSimUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "シミュレーション" in reply_service.texts[0].text

    groups = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})
    assert groups[0].mode == GroupMode.sim.value
    assert groups[0].active_match_id is not None
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is not None
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 1


def test_always_creates_fresh_hanchan():
    """既存の active hanchan があっても、sim 用に新しい半荘を作成する。
    これにより input モードの途中入力が sim に混入しない。
    """
    request_info_service.set_req_info(event=dummy_event)
    existing_hanchan = Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        raw_scores={"U001": 35000, "U002": 25000},
        _id=1,
    )
    match_repository.create(
        Match(
            _id=1,
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            active_hanchan_id=1,
        ),
    )
    hanchan_repository.create(existing_hanchan)
    group_repository.create(
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.input.value,
            active_match_id=1,
            _id=1,
        ),
    )

    StartSimUseCase().execute()

    # sim 用に新しい半荘が作成され、active_hanchan_id が更新される
    matches = match_repository.find({"_id": 1})
    assert matches[0].active_hanchan_id != 1  # 元の半荘ではない
    # 新しい半荘は空の raw_scores
    hanchans = hanchan_repository.find({"_id": matches[0].active_hanchan_id})
    assert len(hanchans) == 1
    assert hanchans[0].raw_scores == {}
