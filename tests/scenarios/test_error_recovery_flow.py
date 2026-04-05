"""シナリオテスト: 半荘削除 → 再入力フロー

誤って入力した半荘を削除し、正しい点数で再入力するシナリオ。
"""
from scenario_helpers import set_group_request

from repositories import hanchan_repository, match_repository
from use_cases.group_line.add_point_by_text_use_case import AddPointByTextUseCase
from use_cases.group_line.drop_hanchan_by_index_use_case import (
    DropHanchanByIndexUseCase,
)
from use_cases.group_line.join_group_use_case import JoinGroupUseCase
from use_cases.group_line.start_input_use_case import StartInputUseCase
from use_cases.group_line.submit_hanchan_use_case import SubmitHanchanUseCase

GROUP_ID = "G_scenario_error_recovery_001abc"
USER_IDS = [
    "U_scenario_err_001_abcdefghijklm",
    "U_scenario_err_002_abcdefghijklm",
    "U_scenario_err_003_abcdefghijklm",
    "U_scenario_err_004_abcdefghijklm",
]
FIRST_SCORES = [40000, 30000, 20000, 10001]   # 第1回 (後で削除)
CORRECT_SCORES = [35000, 32000, 21000, 12001]  # 第2回 (正しい点数)


def _set_group_request(user_index: int = 0):
    set_group_request(GROUP_ID, USER_IDS[user_index])


def test_error_recovery_flow():
    """エラーリカバリーフロー。

    1. グループ参加
    2. 第1半荘入力・確定 (誤った点数)
    3. 第2半荘入力中に第1半荘を削除
    4. 第2半荘を確定
    最終 DB 状態: 第1半荘は is_deleted=True, 第2半荘は非削除
    """
    # === Step 1: グループ参加 ===
    _set_group_request()
    JoinGroupUseCase().execute()

    # === Step 2: 第1半荘 入力・確定 ===
    _set_group_request()
    StartInputUseCase().execute()

    from repositories import group_repository
    groups = group_repository.find({"line_group_id": GROUP_ID})
    match_id = groups[0].active_match_id

    # 第1半荘の点数入力
    for user_id, score in zip(USER_IDS, FIRST_SCORES):
        set_group_request(GROUP_ID, user_id)
        AddPointByTextUseCase().execute(str(score))

    _set_group_request()
    SubmitHanchanUseCase().execute()

    # 第1半荘が archived されていることを確認
    hanchans_after_first = hanchan_repository.find(
        {"match_id": match_id, "converted_scores": {"$ne": {}}},
    )
    assert len(hanchans_after_first) == 1
    first_hanchan_id = hanchans_after_first[0]._id

    # === Step 3: 第2半荘 入力開始 ===
    _set_group_request()
    StartInputUseCase().execute()

    # 第2半荘の点数入力
    for user_id, score in zip(USER_IDS, CORRECT_SCORES):
        set_group_request(GROUP_ID, user_id)
        AddPointByTextUseCase().execute(str(score))

    # 第1半荘を削除 (DropHanchanByIndexUseCase でインデックス 1 を削除)
    _set_group_request()
    DropHanchanByIndexUseCase().execute("1")

    # hanchan_repository.find() は is_deleted=True を除外するため、
    # 削除済みの半荘は 0 件で返ってくる
    deleted_hanchans = hanchan_repository.find({"_id": first_hanchan_id})
    assert len(deleted_hanchans) == 0

    # === Step 4: 第2半荘 確定 ===
    _set_group_request()
    SubmitHanchanUseCase().execute()

    # 第2半荘が確定されている (converted_scores が non-empty)
    groups = group_repository.find({"line_group_id": GROUP_ID})
    new_match = match_repository.find({"_id": match_id})[0]
    # sum_scores に 4 ユーザー分のスコアが入っている
    assert len(new_match.sum_scores) == 4
