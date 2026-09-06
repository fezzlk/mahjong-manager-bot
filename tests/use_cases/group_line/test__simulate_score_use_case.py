from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from domain_model.entities.user import User, UserMode
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_repository,
)
from use_cases.group_line.simulate_score_use_case import SimulateScoreUseCase

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"

dummy_users = [
    User(
        line_user_name=f"test_user{i}",
        line_user_id=f"U012345678{i}abcdefghijklmnopqrstu",
        mode=UserMode.wait.value,
        _id=i,
    )
    for i in range(1, 5)
]


def _setup(raw_scores=None):
    request_info_service.req_line_group_id = _LINE_GROUP_ID
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    for u in dummy_users:
        user_repository.create(u)
    sim_match = match_repository.create(
        Match(line_group_id=_LINE_GROUP_ID),
    )
    sim_hanchan = hanchan_repository.create(
        Hanchan(
            line_group_id=_LINE_GROUP_ID,
            match_id=sim_match._id,
            raw_scores=raw_scores or {},
        ),
    )
    match_repository.update({"_id": sim_match._id}, {"active_hanchan_id": sim_hanchan._id})
    group_repository.create(
        Group(
            line_group_id=_LINE_GROUP_ID,
            mode=GroupMode.sim.value,
            sim_match_id=sim_match._id,
        ),
    )
    return sim_match, sim_hanchan


def test_no_sim_match_does_nothing():
    """sim_match_idが未設定(sim未開始)なら何もしない。"""
    group_repository.create(Group(line_group_id=_LINE_GROUP_ID, mode=GroupMode.sim.value))
    request_info_service.req_line_group_id = _LINE_GROUP_ID
    request_info_service.req_line_user_id = dummy_users[0].line_user_id

    SimulateScoreUseCase().execute("30000")

    assert len(reply_service.texts) == 0


def test_collects_scores_without_touching_real_match():
    """sim_match_id側の半荘にのみ点数が記録され、実系列とは無関係。"""
    _setup()

    SimulateScoreUseCase().execute("30000")

    assert len(reply_service.texts) == 1
    assert "test_user1: 30000" in reply_service.texts[0].text


def test_four_players_shows_result_and_cleans_up():
    """4人分揃うと計算結果を表示し、simの半荘を破棄してwaitモードへ戻す。"""
    sim_match, sim_hanchan = _setup(
        raw_scores={
            dummy_users[1].line_user_id: 30000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 10000,
        },
    )

    SimulateScoreUseCase().execute("40000")

    assert len(reply_service.texts) == 2
    assert "[シミュレーション結果]" in reply_service.texts[1].text

    hanchans = hanchan_repository.find({"_id": sim_hanchan._id})
    assert len(hanchans) == 0  # is_deleted=Trueでfind()から除外される

    matches = match_repository.find({"_id": sim_match._id})
    assert matches[0].active_hanchan_id is None

    groups = group_repository.find({"line_group_id": _LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.wait.value


def test_sum_mismatch_keeps_hanchan_open():
    """合計が100000点にならない場合はエラーを返し、半荘は破棄しない(訂正可能)。"""
    sim_match, sim_hanchan = _setup(
        raw_scores={
            dummy_users[1].line_user_id: 10000,
            dummy_users[2].line_user_id: 10000,
            dummy_users[3].line_user_id: 10000,
        },
    )

    SimulateScoreUseCase().execute("10000")

    assert any("合計" in t.text for t in reply_service.texts)
    hanchans = hanchan_repository.find({"_id": sim_hanchan._id})
    assert len(hanchans) == 1  # 破棄されていない


def test_tie_score_rejected():
    """同点がある場合はエラーを返す。"""
    sim_match, sim_hanchan = _setup(
        raw_scores={
            dummy_users[1].line_user_id: 25000,
            dummy_users[2].line_user_id: 25000,
            dummy_users[3].line_user_id: 25000,
        },
    )

    SimulateScoreUseCase().execute("25000")

    assert any("同点" in t.text for t in reply_service.texts)


def test_uses_group_settings_for_calculation():
    """グループ設定(レート等)を反映して計算する。"""
    _setup(
        raw_scores={
            dummy_users[1].line_user_id: 30000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 10000,
        },
    )
    group_repository.update_settings(_LINE_GROUP_ID, EmbeddedGroupSettings(rate=5))

    SimulateScoreUseCase().execute("40000")

    assert len(reply_service.texts) == 2
    assert "[シミュレーション結果]" in reply_service.texts[1].text
