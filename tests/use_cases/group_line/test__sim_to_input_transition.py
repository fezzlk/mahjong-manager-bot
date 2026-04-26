"""sim モードと input モード間のモード遷移テスト。

sim モードの途中入力データが input モードに漏れないことを検証する。
"""
from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from domain_model.entities.user import User, UserMode
from line_models.event import Event
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_repository,
)
from use_cases.group_line.simulate_score_use_case import SimulateScoreUseCase
from use_cases.group_line.start_input_use_case import StartInputUseCase
from use_cases.group_line.start_sim_use_case import StartSimUseCase

LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"
USER_IDS = [f"U0123456789abcdefghijklmnopqrstu{i}" for i in range(1, 5)]

sim_event = Event(
    type="message",
    source_type="group",
    user_id=USER_IDS[0],
    group_id=LINE_GROUP_ID,
    message_type="text",
    text="_sim",
)

input_event = Event(
    type="message",
    source_type="group",
    user_id=USER_IDS[0],
    group_id=LINE_GROUP_ID,
    message_type="text",
    text="_input",
)


def _setup_users():
    for i, uid in enumerate(USER_IDS):
        user_repository.create(
            User(
                line_user_name=f"test_user{i + 1}",
                line_user_id=uid,
                mode=UserMode.wait.value,
                _id=i + 1,
            ),
        )


def _setup_group_with_match_and_hanchan(mode=GroupMode.wait.value):
    """グループ・マッチ・半荘を作成し、input 用の半荘に途中データを入れる。"""
    hanchan_repository.create(
        Hanchan(
            line_group_id=LINE_GROUP_ID,
            match_id=1,
            raw_scores={USER_IDS[0]: 35000, USER_IDS[1]: 25000},
            _id=1,
        ),
    )
    match_repository.create(
        Match(
            _id=1,
            line_group_id=LINE_GROUP_ID,
            active_hanchan_id=1,
        ),
    )
    group_repository.create(
        Group(
            line_group_id=LINE_GROUP_ID,
            mode=mode,
            active_match_id=1,
            _id=1,
        ),
    )


def test_sim_to_input_cleans_up_sim_hanchan():
    """Sim → input 切り替え時に sim 用半荘が削除され、
    新しい空の半荘で input モードが開始される。
    """
    _setup_users()
    request_info_service.set_req_info(event=sim_event)

    # wait → sim: 新しいマッチ＆半荘が作成される
    group_repository.create(
        Group(line_group_id=LINE_GROUP_ID, _id=1),
    )
    StartSimUseCase().execute()
    reply_service.reset()

    # sim モードで点数を1人分入力
    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.sim.value
    matches = match_repository.find()
    sim_hanchan_id = matches[0].active_hanchan_id
    score_event = Event(
        type="message",
        source_type="group",
        user_id=USER_IDS[0],
        group_id=LINE_GROUP_ID,
        message_type="text",
        text="35000",
    )
    request_info_service.set_req_info(event=score_event)
    SimulateScoreUseCase().execute(request_info_service.message)
    reply_service.reset()

    # sim → input に切り替え
    request_info_service.set_req_info(event=input_event)
    StartInputUseCase().execute()

    # sim 用半荘は is_deleted=True になっている
    # (find は is_deleted != True を自動付加するので、find で見つからなくなる)
    sim_hanchans = hanchan_repository.find({"_id": sim_hanchan_id})
    assert len(sim_hanchans) == 0

    # input 用に新しい空の半荘が作成されている
    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.input.value
    matches = match_repository.find()
    new_hanchan_id = matches[0].active_hanchan_id
    assert new_hanchan_id != sim_hanchan_id
    new_hanchans = hanchan_repository.find({"_id": new_hanchan_id})
    assert len(new_hanchans) == 1
    assert new_hanchans[0].raw_scores == {}


def test_input_to_sim_does_not_reuse_input_hanchan():
    """Input → sim 切り替え時に、input の途中データが sim に混入しない。"""
    _setup_users()
    _setup_group_with_match_and_hanchan(mode=GroupMode.input.value)

    # input 半荘に途中データがある状態を確認
    hanchans = hanchan_repository.find({"_id": 1})
    assert hanchans[0].raw_scores == {USER_IDS[0]: 35000, USER_IDS[1]: 25000}

    # input → sim に切り替え
    request_info_service.set_req_info(event=sim_event)
    StartSimUseCase().execute()

    # sim 用に新しい半荘が作成され、空の raw_scores
    matches = match_repository.find({"_id": 1})
    sim_hanchan_id = matches[0].active_hanchan_id
    assert sim_hanchan_id != 1  # 元の input 半荘ではない
    sim_hanchans = hanchan_repository.find({"_id": sim_hanchan_id})
    assert len(sim_hanchans) == 1
    assert sim_hanchans[0].raw_scores == {}


def test_input_to_sim_to_input_no_data_leak():
    """Input → sim → input の往復で、sim のデータが input に漏れない。"""
    _setup_users()
    _setup_group_with_match_and_hanchan(mode=GroupMode.input.value)

    # input → sim
    request_info_service.set_req_info(event=sim_event)
    StartSimUseCase().execute()
    reply_service.reset()

    # sim で点数入力
    matches = match_repository.find({"_id": 1})
    sim_hanchan_id = matches[0].active_hanchan_id
    score_event = Event(
        type="message",
        source_type="group",
        user_id=USER_IDS[0],
        group_id=LINE_GROUP_ID,
        message_type="text",
        text="40000",
    )
    request_info_service.set_req_info(event=score_event)
    SimulateScoreUseCase().execute(request_info_service.message)
    reply_service.reset()

    # sim → input に戻す
    request_info_service.set_req_info(event=input_event)
    StartInputUseCase().execute()

    # sim 半荘は削除済み
    sim_hanchans = hanchan_repository.find({"_id": sim_hanchan_id})
    assert len(sim_hanchans) == 0

    # input 用に新しい空の半荘が作成されている（sim データなし）
    groups = group_repository.find({"line_group_id": LINE_GROUP_ID})
    assert groups[0].mode == GroupMode.input.value
    matches = match_repository.find({"_id": 1})
    new_hanchan_id = matches[0].active_hanchan_id
    assert new_hanchan_id != sim_hanchan_id
    new_hanchans = hanchan_repository.find({"_id": new_hanchan_id})
    assert len(new_hanchans) == 1
    assert new_hanchans[0].raw_scores == {}
