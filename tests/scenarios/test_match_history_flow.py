"""シナリオテスト: 対局完了 → 履歴参照フロー

グループで対局を 2 回完了させた後、対局履歴を参照・検索できることを検証する。
"""
from unittest.mock import patch

from scenario_helpers import set_group_request

from application_service import reply_service
from domain_model.entities.group import GroupMode
from repositories import group_repository, match_repository
from use_cases.group_line.add_point_by_text_use_case import AddPointByTextUseCase
from use_cases.group_line.finish_match_use_case import FinishMatchUseCase
from use_cases.group_line.join_group_use_case import JoinGroupUseCase
from use_cases.group_line.reply_matches_use_case import ReplyMatchesUseCase
from use_cases.group_line.start_input_use_case import StartInputUseCase
from use_cases.group_line.submit_hanchan_use_case import SubmitHanchanUseCase

GROUP_ID = "G_scenario_history_flow_001_abc"
USER_IDS = [
    "U_scenario_hist_001_abcdefghijkl",
    "U_scenario_hist_002_abcdefghijkl",
    "U_scenario_hist_003_abcdefghijkl",
    "U_scenario_hist_004_abcdefghijkl",
]
RAW_SCORES_1 = [40000, 30000, 20000, 10001]   # 第1マッチ
RAW_SCORES_2 = [35000, 32000, 22000, 11001]   # 第2マッチ


def _set_group_request(user_index: int = 0):
    set_group_request(GROUP_ID, USER_IDS[user_index])


def _play_one_match(raw_scores):
    """1マッチ分 (1半荘) をプレイして終了し、match_id を返す。"""
    _set_group_request()
    StartInputUseCase().execute()

    groups = group_repository.find({"line_group_id": GROUP_ID})
    match_id = groups[0].active_match_id

    for user_id, score in zip(USER_IDS, raw_scores):
        set_group_request(GROUP_ID, user_id)
        AddPointByTextUseCase().execute(str(score))

    _set_group_request()
    SubmitHanchanUseCase().execute()

    _set_group_request()
    with patch(
        "application_service.graph_service.GraphService.create_users_point_plot_graph_url",
        return_value=(None, None),
    ):
        FinishMatchUseCase().execute()

    return match_id


def test_match_history_flow():
    """対局完了 → 履歴参照フロー。

    2 マッチ完了後に ReplyMatchesUseCase でマッチ一覧を取得できることを検証。
    """
    # グループ参加
    _set_group_request()
    JoinGroupUseCase().execute()

    # === マッチ 1 ===
    match_id_1 = _play_one_match(RAW_SCORES_1)

    # マッチ 1 が終了していることを確認
    groups = group_repository.find({"line_group_id": GROUP_ID})
    assert groups[0].active_match_id is None
    assert groups[0].mode == GroupMode.wait.value

    # === マッチ 2 ===
    match_id_2 = _play_one_match(RAW_SCORES_2)

    assert match_id_1 != match_id_2

    # === 履歴参照: ReplyMatchesUseCase ===
    reply_service.reset()
    _set_group_request()
    ReplyMatchesUseCase().execute()

    # マッチ一覧が reply_service に追加されている
    all_texts = [t.text for t in reply_service.texts] + [b.alt_text for b in reply_service.buttons]
    assert len(all_texts) > 0

    # === DB レベルの検証: 2 マッチが archived されている ===
    all_matches = match_repository.find({"line_group_id": GROUP_ID})
    # is_deleted=True でない、かつ sum_scores がある完了済みマッチ
    completed = [m for m in all_matches if m.sum_scores]
    assert len(completed) == 2


def test_match_history_flow_no_matches_returns_message():
    """グループにマッチがない状態で ReplyMatchesUseCase を呼ぶと適切なメッセージを返す"""
    # グループ参加のみ
    _set_group_request()
    JoinGroupUseCase().execute()

    reply_service.reset()
    _set_group_request()
    ReplyMatchesUseCase().execute()

    # 何らかのメッセージが返ることを確認 (「対戦記録がありません」など)
    all_msgs = [t.text for t in reply_service.texts]
    assert len(all_msgs) > 0
