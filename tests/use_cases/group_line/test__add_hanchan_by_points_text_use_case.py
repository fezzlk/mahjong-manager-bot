import importlib

import pytest

from application_service import reply_service, request_info_service
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match, MatchStatus
from domain_model.entities.user import User
from domain_service import hanchan_service, match_service
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_repository,
)
from routing_by_text_in_group_line import routing_by_text_in_group_line
from use_cases.group_line.add_hanchan_by_points_text_use_case import (
    AddHanchanByPointsTextUseCase as ImportScores,
)
from use_cases.group_line.add_point_by_text_use_case import AddPointByTextUseCase
from use_cases.group_line.submit_hanchan_use_case import SubmitHanchanUseCase
from use_cases.utility.input_point_use_case import InputPointUseCase

TEXT = "Alice: 40000\nBob: 30000\nCarol: 20000\nDave: 10000"
POINTS = {"U1": 40000, "U2": 30000, "U3": 20000, "U4": 10000}


@pytest.fixture
def group(monkeypatch):
    # Do not contact LINE while round-tripping the real reply formatter.
    def offline_profile(*args):
        raise RuntimeError("offline test")

    monkeypatch.setattr(
        importlib.import_module("domain_service.user_service"),
        "_cached_get_profile_name",
        offline_profile,
    )
    request_info_service.req_line_group_id = "G-paste-test"
    request_info_service.req_line_user_id = "U1"
    result = group_repository.create(
        Group(
            line_group_id="G-paste-test",
        ),
    )
    result.settings = EmbeddedGroupSettings()
    group_repository.update_settings(result.line_group_id, result.settings)
    for i, name in enumerate(["Alice", "Bob", "Carol", "Dave"], 1):
        user_repository.create(User(line_user_id=f"U{i}", line_user_name=name))
    return result


def paste(text=TEXT):
    request_info_service.message = text
    request_info_service.command = None
    routing_by_text_in_group_line()


def create_target(group, scores=None):
    target = match_repository.create(
        Match(
            line_group_id=group.line_group_id,
            settings=group.settings,
        ),
    )
    if scores is not None:
        half = hanchan_repository.create(
            Hanchan(
                line_group_id=group.line_group_id,
                match_id=target._id,
                raw_scores=scores,
            ),
        )
        target.active_hanchan_id = half._id
        match_service.update(target)
    group.current_input_match_id = target._id
    group_repository.update({"_id": group._id}, {"active_match_id": target._id})
    return target


def test_paste_creates_and_settles_half_game(group):
    paste()
    halves = hanchan_repository.find({})
    assert len(halves) == 1
    half = halves[0]
    assert half.raw_scores == POINTS
    assert half.converted_scores == {"U1": 50, "U2": 10, "U3": -20, "U4": -40}
    assert len(half.results) == 4
    target = match_service.find_one_by_id(half.match_id)
    assert target.active_hanchan_id is None
    assert target.sum_scores == half.converted_scores


def test_actual_bot_reply_round_trip(group, monkeypatch):
    target = create_target(group, {})
    raw_reply = None
    for uid, points in POINTS.items():
        monkeypatch.setattr(
            InputPointUseCase, "execute", lambda _self, _text, u=uid, p=points: (u, p),
        )
        reply_service.reset()
        AddPointByTextUseCase().execute(str(points))
        raw_reply = reply_service.texts[0].text
    assert raw_reply == TEXT
    paste(raw_reply)
    halves = hanchan_repository.find({"match_id": target._id})
    assert len(halves) == 2
    assert all(h.raw_scores == POINTS and h.converted_scores for h in halves)
    assert match_service.find_one_by_id(target._id).sum_scores == {
        "U1": 100,
        "U2": 20,
        "U3": -40,
        "U4": -80,
    }


@pytest.mark.parametrize(
    "text",
    [
        "Alice: 40000\nBob: 30000",
        TEXT.replace("Dave", "Unknown"),
        TEXT.replace("Dave", "Alice"),
        TEXT.replace("10000", "9000"),
        TEXT.replace("40000", "30000").replace("10000", "20000"),
        TEXT.replace("40000", "not-a-number"),
        TEXT + "\nこれを登録して",
        "Alice: +50 (+100)\nBob: +10 (+20)\nCarol: -20 (-40)\nDave: -40 (-80)",
    ],
)
def test_invalid_input_never_creates_match_or_half_game(group, text):
    paste(text)
    assert match_repository.find({}) == []
    assert hanchan_repository.find({}) == []


def test_same_name_is_rejected(group):
    user_repository.create(User(line_user_id="U5", line_user_name="Alice"))
    paste()
    assert hanchan_repository.find({}) == []


def test_in_progress_scores_unchanged(group):
    target = create_target(group, {"U1": 12345})
    paste()
    assert len(hanchan_repository.find({})) == 1
    assert hanchan_service.find_one_by_id(target.active_hanchan_id).raw_scores == {
        "U1": 12345,
    }
    assert "上書きしていません" in reply_service.texts[-1].text


def test_empty_target_is_filled(group):
    target = create_target(group, {})
    paste()
    assert len(hanchan_repository.find({})) == 1
    assert hanchan_service.find_one_by_id(target.active_hanchan_id).raw_scores == POINTS


def test_three_player_settings(group):
    group.settings.num_of_players = 3
    group_repository.update_settings(group.line_group_id, group.settings)
    paste("Alice: 50000\nBob: 35000\nCarol: 20000")
    halves = hanchan_repository.find({})
    assert len(halves) == 1
    assert len(halves[0].results) == 3
    assert halves[0].converted_scores


@pytest.mark.parametrize("mode", [GroupMode.sim.value, GroupMode.chip_input.value])
def test_other_modes_do_not_import(group, mode):
    group_repository.update({"_id": group._id}, {"mode": mode})
    paste()
    assert hanchan_repository.find({}) == []
    assert match_repository.find({}) == []


def test_ambiguous_destination_is_not_selected(group):
    for _ in range(2):
        match_repository.create(Match(line_group_id=group.line_group_id))
    paste()
    assert hanchan_repository.find({}) == []
    assert "登録先" in reply_service.texts[-1].text


@pytest.mark.parametrize(
    ("status", "owner"),
    [
        (MatchStatus.settled.value, "G-paste-test"),
        (MatchStatus.open.value, "other-group"),
    ],
)
def test_invalid_destination_is_rejected(group, status, owner):
    target = create_target(group)
    match_repository.update_field(
        {"_id": target._id}, set_values={"status": status, "line_group_id": owner},
    )
    paste()
    assert hanchan_repository.find({}) == []


def test_negative_score_uses_existing_tobi_flow(group):
    paste(TEXT.replace("40000", "55000").replace("10000", "-5000"))
    half = hanchan_repository.find({})[0]
    assert half.converted_scores == {}
    assert match_service.find_one_by_id(half.match_id).active_hanchan_id == half._id
    SubmitHanchanUseCase().execute(tobashita_player_id="U1")
    assert hanchan_service.find_one_by_id(half._id).converted_scores


def test_plain_number_keeps_existing_route(group, monkeypatch):
    group_repository.update({"_id": group._id}, {"mode": GroupMode.input.value})
    called = []
    monkeypatch.setattr(
        AddPointByTextUseCase, "execute", lambda _self, text: called.append(text),
    )
    paste("35000")
    assert called == ["35000"]
    assert hanchan_repository.find({}) == []


def test_concurrent_score_is_not_overwritten(group, monkeypatch):
    target = create_target(group, {})
    original = hanchan_repository.update_field

    def racing_update(query, **kwargs):
        if query.get("raw_scores") == {}:
            original(
                {"_id": target.active_hanchan_id}, set_values={"raw_scores.U1": 12345},
            )
        return original(query, **kwargs)

    monkeypatch.setattr(hanchan_repository, "update_field", racing_update)
    paste()
    assert hanchan_service.find_one_by_id(target.active_hanchan_id).raw_scores == {
        "U1": 12345,
    }


def test_submit_does_not_finalize_a_different_half_game(group):
    target = create_target(group, POINTS)
    SubmitHanchanUseCase().execute(
        expected_match_id=target._id, expected_hanchan_id="different",
    )
    assert (
        hanchan_service.find_one_by_id(target.active_hanchan_id).converted_scores == {}
    )


@pytest.mark.parametrize(
    "text",
    [
        "Alice: 40000\r\nBob: 30000\r\nCarol: 20000\r\nDave: 10000\r\n",
        "Alice: 40000\nBob: 30000\nCarol: 20000\nDave: 10000",
    ],
)
def test_parser_accepts_bot_line_endings(text):
    assert ImportScores.parse_reply(text) == [
        ("Alice", 40000),
        ("Bob", 30000),
        ("Carol", 20000),
        ("Dave", 10000),
    ]


def test_match_settings_override_group_settings(group):
    target = create_target(group)
    setting = EmbeddedGroupSettings(num_of_players=3)
    match_repository.update_field(
        {"_id": target._id}, set_values={"settings": setting.to_dict()},
    )
    paste("Alice: 50000\nBob: 35000\nCarol: 20000")
    assert len(hanchan_repository.find({})[0].results) == 3


def test_competing_half_game_is_not_replaced(group, monkeypatch):
    target = create_target(group)
    original = match_repository.update_field
    competitor = hanchan_repository.create(
        Hanchan(
            line_group_id=group.line_group_id,
            match_id=target._id,
            raw_scores={"U1": 12345},
        ),
    )

    def racing_attach(query, **kwargs):
        if query.get("active_hanchan_id", "absent") is None:
            original(
                {"_id": target._id}, set_values={"active_hanchan_id": competitor._id},
            )
        return original(query, **kwargs)

    monkeypatch.setattr(match_repository, "update_field", racing_attach)
    paste()
    assert match_service.find_one_by_id(target._id).active_hanchan_id == competitor._id
    assert hanchan_service.find_one_by_id(competitor._id).raw_scores == {"U1": 12345}
    assert len(hanchan_repository.find({})) == 1


def test_names_with_spaces_colons_or_command_prefix_round_trip(group):
    user_repository.update({"line_user_id": "U1"}, {"line_user_name": "_Alice: A"})
    request_info_service.message = TEXT.replace("Alice", "_Alice: A")
    request_info_service.parse_message()
    routing_by_text_in_group_line()
    assert hanchan_repository.find({})[0].raw_scores == POINTS
