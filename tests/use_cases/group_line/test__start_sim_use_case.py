from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match, MatchStatus
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


def test_new_sim_match_and_hanchan():
    """sim用のMatchもhanchanもない場合、両方新規作成してsimモードになる。

    sim専用のsim_match_idに紐付き、実系列のactive_match_idは変化しない。
    """
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(
        Group(line_group_id="G0123456789abcdefghijklmnopqrstu1", _id=1),
    )
    StartSimUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "シミュレーション" in reply_service.texts[0].text

    groups = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})
    assert groups[0].mode == GroupMode.sim.value
    assert groups[0].sim_match_id is not None
    assert groups[0].active_match_id is None
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is not None
    assert matches[0].status == MatchStatus.sim.value
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 1


def test_does_not_touch_real_active_match():
    """実系列(_input中)の対戦・半荘は、_sim実行後も一切変更されない(FEZ-66 Phase C)。

    以前は sim が active_match_id を流用しており、_input で入力中の実対戦の
    active_hanchan_id を sim 用半荘で上書きしてしまうデータ破損バグがあった。
    """
    request_info_service.set_req_info(event=dummy_event)
    real_hanchan = Hanchan(
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
    hanchan_repository.create(real_hanchan)
    group_repository.create(
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.input.value,
            active_match_id=1,
            _id=1,
        ),
    )

    StartSimUseCase().execute()

    # 実対戦(_id=1)のactive_hanchan_idは変更されない
    real_matches = match_repository.find({"_id": 1})
    assert real_matches[0].active_hanchan_id == 1
    real_hanchans = hanchan_repository.find({"_id": 1})
    assert real_hanchans[0].raw_scores == {"U001": 35000, "U002": 25000}

    # sim用に別のMatchが新規作成され、group.sim_match_idが指す
    groups = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})
    assert groups[0].sim_match_id is not None
    assert groups[0].sim_match_id != 1
    sim_matches = match_repository.find({"_id": groups[0].sim_match_id})
    assert len(sim_matches) == 1
    sim_hanchans = hanchan_repository.find({"_id": sim_matches[0].active_hanchan_id})
    assert sim_hanchans[0].raw_scores == {}


def test_reuses_sim_match_across_sessions():
    """2回目以降の_simは同じsim_match_idを再利用し、新規Matchは作らない。"""
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(
        Group(line_group_id="G0123456789abcdefghijklmnopqrstu1", _id=1),
    )

    StartSimUseCase().execute()
    first_groups = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})
    first_sim_match_id = first_groups[0].sim_match_id

    # 一度wait状態に戻してから再度_simを実行する
    group = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})[0]
    group.mode = GroupMode.wait.value
    group_repository.update({"_id": group._id}, {"mode": GroupMode.wait.value})

    StartSimUseCase().execute()
    second_groups = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})

    assert second_groups[0].sim_match_id == first_sim_match_id
    assert len(match_repository.find()) == 1  # Matchは新規作成されない
    assert len(hanchan_repository.find()) == 2  # hanchanは毎回新規作成される
