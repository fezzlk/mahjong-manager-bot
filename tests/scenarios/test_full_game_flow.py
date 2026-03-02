"""シナリオテスト: グループ参加 → 点数入力 → 半荘確定 → 対局終了 の完全フロー

複数 Use Case をまたぐ業務シナリオを DB 付きで検証する。
"""
from unittest.mock import patch

from scenario_helpers import set_group_request

from domain_model.entities.group import GroupMode
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_hanchan_repository,
)
from use_cases.group_line.add_point_by_text_use_case import AddPointByTextUseCase
from use_cases.group_line.finish_match_use_case import FinishMatchUseCase
from use_cases.group_line.join_group_use_case import JoinGroupUseCase
from use_cases.group_line.start_input_use_case import StartInputUseCase
from use_cases.group_line.submit_hanchan_use_case import SubmitHanchanUseCase

GROUP_ID = "G_scenario_full_flow_001_abcdef"
USER_IDS = [
    "U_scenario_full_001_abcdefghijkl",
    "U_scenario_full_002_abcdefghijkl",
    "U_scenario_full_003_abcdefghijkl",
    "U_scenario_full_004_abcdefghijkl",
]
# 合計 100001 点 (100000〜100099 範囲内)、全員異なる、全員正の点数
RAW_SCORES = [40000, 30000, 20000, 10001]


def _set_group_request(user_index: int = 0):
    set_group_request(GROUP_ID, USER_IDS[user_index])


def test_full_game_flow():
    """グループ参加 → 入力開始 → 4人分の点数入力 → 半荘確定 → 対局終了。

    最終 DB 状態:
    - group.mode = "wait"
    - group.active_match_id = None
    - 半荘に converted_scores が設定されている
    - user_hanchan レコードが 4 件作成されている
    """
    # === Step 1: グループ参加 ===
    _set_group_request()
    JoinGroupUseCase().execute()

    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert len(groups) == 1
    assert groups[0].mode == GroupMode.wait.value

    # === Step 2: 点数入力開始 ===
    _set_group_request()
    StartInputUseCase().execute()

    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert groups[0].mode == GroupMode.input.value
    match_id = groups[0].active_match_id
    assert match_id is not None

    matches = match_repository.find({"_id": match_id})
    assert len(matches) == 1
    hanchan_id = matches[0].active_hanchan_id
    assert hanchan_id is not None

    # === Step 3: 4 人分の点数入力 ===
    for user_id, score in zip(USER_IDS, RAW_SCORES):
        set_group_request(GROUP_ID, user_id)
        AddPointByTextUseCase().execute(str(score))

    hanchans = hanchan_repository.find({"_id": hanchan_id})
    assert len(hanchans) == 1
    assert len(hanchans[0].raw_scores) == 4
    for user_id, score in zip(USER_IDS, RAW_SCORES):
        assert hanchans[0].raw_scores[user_id] == score

    # === Step 4: 半荘確定 (graph 生成はモックしない、失敗しても構わない) ===
    _set_group_request()
    SubmitHanchanUseCase().execute()

    # 半荘が確定されたことを確認
    hanchans = hanchan_repository.find({"_id": hanchan_id})
    assert len(hanchans[0].converted_scores) == 4
    # グループが wait モードに戻る
    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert groups[0].mode == GroupMode.wait.value
    # UserHanchan が 4 件作成されている
    user_hanchans = user_hanchan_repository.find({"hanchan_id": hanchan_id})
    assert len(user_hanchans) == 4

    # === Step 5: 対局終了 (グラフ生成は無視) ===
    # match.active_match_id はリセットされているのでグループに再設定して確認
    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert groups[0].active_match_id is not None  # FinishMatch 前はまだ active

    _set_group_request()
    with patch(
        "application_service.graph_service.GraphService.create_users_point_plot_graph_url",
        return_value=(None, "test_mock"),
    ):
        FinishMatchUseCase().execute()

    # グループの active_match_id がクリアされている
    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert groups[0].active_match_id is None
    assert groups[0].mode == GroupMode.wait.value

    # マッチに sum_prices が設定されている
    matches = match_repository.find({"_id": match_id})
    assert len(matches) == 1
    assert matches[0].sum_scores is not None
    assert len(matches[0].sum_scores) == 4
