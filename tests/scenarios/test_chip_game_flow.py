"""シナリオテスト: チップあり対局フロー

グループ参加 → 入力開始 → 点数入力 → 半荘確定 → チップ入力 → チップ確定(マッチ終了)
の完全フローを複数 Use Case をまたいで検証する。
"""
from unittest.mock import patch

from scenario_helpers import set_group_request

from application_service import reply_service
from domain_model.entities.group import GroupMode
from repositories import group_repository, match_repository
from use_cases.group_line.add_chip_by_text_use_case import AddChipByTextUseCase
from use_cases.group_line.add_point_by_text_use_case import AddPointByTextUseCase
from use_cases.group_line.finish_input_chip_use_case import FinishInputChipUseCase
from use_cases.group_line.join_group_use_case import JoinGroupUseCase
from use_cases.group_line.start_input_use_case import StartInputUseCase
from use_cases.group_line.submit_hanchan_use_case import SubmitHanchanUseCase

GROUP_ID = "G_scenario_chip_flow_001_abcdef"
USER_IDS = [
    "U_scenario_chip_001_abcdefghijkl",
    "U_scenario_chip_002_abcdefghijkl",
    "U_scenario_chip_003_abcdefghijkl",
    "U_scenario_chip_004_abcdefghijkl",
]
# 合計 100001 点、全員異なる、全員正の点数
RAW_SCORES = [40000, 30000, 20000, 10001]
# チップ増減: 合計 0 になること
CHIP_SCORES = [3, -1, -2, 0]


def _set_group_request(user_index: int = 0):
    set_group_request(GROUP_ID, USER_IDS[user_index])


def test_chip_game_flow():
    """チップあり対局フロー。

    最終 DB 状態:
    - group.mode = "wait"
    - group.active_match_id = None (マッチ終了)
    - match.chip_scores にチップ情報が保存されている
    - match.sum_scores に集計結果が入っている
    """
    # === Step 1: グループ参加 ===
    _set_group_request()
    JoinGroupUseCase().execute()

    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert len(groups) == 1

    # === Step 2: 入力開始 ===
    _set_group_request()
    StartInputUseCase().execute()

    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert groups[0].mode == GroupMode.input.value
    match_id = groups[0].active_match_id
    assert match_id is not None

    # === Step 3: 4人分の点数入力 ===
    for user_id, score in zip(USER_IDS, RAW_SCORES):
        set_group_request(GROUP_ID, user_id)
        AddPointByTextUseCase().execute(str(score))

    # === Step 4: 半荘確定 ===
    _set_group_request()
    SubmitHanchanUseCase().execute()

    # 半荘確定後: グループは wait モードに戻るが active_match_id は残る
    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert groups[0].mode == GroupMode.wait.value
    assert groups[0].active_match_id == match_id

    # === Step 5: チップ入力 (合計 = 0) ===
    for user_id, chip in zip(USER_IDS, CHIP_SCORES):
        set_group_request(GROUP_ID, user_id)
        AddChipByTextUseCase().execute(str(chip))

    # チップが match に記録されていることを確認
    matches = match_repository.find({"_id": match_id})
    assert len(matches) == 1
    stored_chip_sum = sum(matches[0].chip_scores.values())
    assert stored_chip_sum == 0

    # === Step 6: チップ確定 → マッチ終了 ===
    _set_group_request()
    with patch(
        "application_service.graph_service.GraphService.create_users_point_plot_graph_url",
        return_value=(None, None),
    ):
        FinishInputChipUseCase().execute()

    # グループの active_match_id がクリア、モードが wait に戻る
    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert groups[0].active_match_id is None
    assert groups[0].mode == GroupMode.wait.value

    # マッチの sum_scores に集計結果が入っている
    matches = match_repository.find({"_id": match_id})
    assert len(matches) == 1
    assert matches[0].sum_scores is not None
    assert len(matches[0].sum_scores) == 4


def test_chip_game_flow_fails_when_chip_sum_not_zero():
    """チップ合計が 0 にならない場合はエラーメッセージが出てマッチは継続"""
    # グループ参加・入力開始
    _set_group_request()
    JoinGroupUseCase().execute()
    _set_group_request()
    StartInputUseCase().execute()

    # 点数入力・半荘確定
    for user_id, score in zip(USER_IDS, RAW_SCORES):
        set_group_request(GROUP_ID, user_id)
        AddPointByTextUseCase().execute(str(score))
    _set_group_request()
    SubmitHanchanUseCase().execute()

    # チップ入力: 合計が 0 にならない (+1, -1, -1, 0 = -1)
    invalid_chips = [1, -1, -1, 0]
    for user_id, chip in zip(USER_IDS, invalid_chips):
        set_group_request(GROUP_ID, user_id)
        AddChipByTextUseCase().execute(str(chip))

    reply_service.reset()
    _set_group_request()
    FinishInputChipUseCase().execute()

    # エラーメッセージが出て、マッチは終了しない
    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert groups[0].active_match_id is not None  # まだ active
    error_texts = [t.text for t in reply_service.texts]
    assert any("0" in t for t in error_texts)
