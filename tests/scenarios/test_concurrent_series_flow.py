"""シナリオテスト: 複数対戦系列の同時進行 (FEZ-66 Phase E)

グループが異なるレートの対戦を2件同時にopenで持つ状態を作り、`_finish`・
`_active_match`のピッカー/select経路が、一方の対戦への操作をもう一方に
一切波及させないことをエンドツーエンドで検証する。

`_input`側の複数系列ピッカー(2件目以降の対戦を`_new_match`で開始する経路)
はこの時点では未実装(次フェーズ)のため、2件目の対戦はテスト側で直接
作成し、group.current_input_match_idを手動で付け替えることでセッションの
切り替えを模している。
"""
from unittest.mock import patch

from scenario_helpers import set_group_request

from application_service import reply_service, request_info_service
from domain_model.entities.group import GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.match import Match, MatchStatus
from domain_service import group_service, hanchan_service, match_service
from repositories import match_repository
from use_cases.group_line.add_point_by_text_use_case import AddPointByTextUseCase
from use_cases.group_line.finish_match_use_case import FinishMatchUseCase
from use_cases.group_line.join_group_use_case import JoinGroupUseCase
from use_cases.group_line.reply_hanchans_of_active_match_use_case import (
    ReplyHanchansOfActiveMatchUseCase,
)
from use_cases.group_line.start_input_use_case import StartInputUseCase
from use_cases.group_line.submit_hanchan_use_case import SubmitHanchanUseCase

GROUP_ID = "G_scenario_concurrent_series_001"
USER_IDS = [
    "U_scenario_concurrent_001_abcdef",
    "U_scenario_concurrent_002_abcdef",
    "U_scenario_concurrent_003_abcdef",
    "U_scenario_concurrent_004_abcdef",
]
RAW_SCORES_SERIES_A = [40000, 30000, 20000, 10001]
RAW_SCORES_SERIES_B = [35000, 32000, 22000, 11001]


def _set_group_request(user_index: int = 0):
    set_group_request(GROUP_ID, USER_IDS[user_index])


def _play_hanchan_on_current_match(raw_scores):
    """現在group.current_input_match_idが指す対戦に1半荘分入力し確定する。"""
    for user_id, score in zip(USER_IDS, raw_scores):
        set_group_request(GROUP_ID, user_id)
        AddPointByTextUseCase().execute(str(score))
    _set_group_request()
    SubmitHanchanUseCase().execute()


def test_concurrent_series_settle_independently():
    """異なるレートの対戦2件を同時open、片方の精算がもう片方に影響しない。"""
    # グループ参加、系列Aを開始(open対戦が0件なので黙って新規作成される)
    _set_group_request()
    JoinGroupUseCase().execute()
    StartInputUseCase().execute()

    group = group_service.find_one_by_line_group_id(GROUP_ID)
    match_a_id = group.current_input_match_id
    match_a = match_repository.find({"_id": match_a_id})[0]
    assert match_a.status == MatchStatus.open.value

    # 系列Aのレートを他と区別可能な値に設定し、1半荘分プレイして待機状態に戻す
    match_a.settings = EmbeddedGroupSettings(rate=3)
    match_service.update(match_a)
    _play_hanchan_on_current_match(RAW_SCORES_SERIES_A)

    group = group_service.find_one_by_line_group_id(GROUP_ID)
    assert group.mode == GroupMode.wait.value

    # 系列B: `_new_match`未実装のため、StartInputUseCaseが行うのと同じ
    # 手順(Match作成+専用Hanchan作成+active_hanchan_id設定)を直接再現し、
    # セッションポインタを手動で付け替える(実装済みなのは_finish/_active_match側)
    match_b = match_repository.create(
        Match(
            line_group_id=GROUP_ID,
            name="系列B",
            status=MatchStatus.open.value,
            settings=EmbeddedGroupSettings(rate=7),
        ),
    )
    hanchan_b = hanchan_service.create_with_line_group_id_and_match_id(GROUP_ID, match_b._id)
    match_b.active_hanchan_id = hanchan_b._id
    match_service.update(match_b)
    group.current_input_match_id = match_b._id
    group.mode = GroupMode.input.value
    group_service.update(group)
    _play_hanchan_on_current_match(RAW_SCORES_SERIES_B)

    # ここでグループはopen対戦2件(系列A: wait、系列B: 入力後にwaitへ戻っている)
    open_matches = match_repository.find(
        {"line_group_id": GROUP_ID, "status": MatchStatus.open.value},
    )
    assert {m._id for m in open_matches} == {match_a_id, match_b._id}

    # `_finish`(open2件)はピッカーを提示し、どちらも精算しない
    reply_service.reset()
    _set_group_request()
    FinishMatchUseCase().execute()
    assert reply_service.texts[0].quick_reply is not None
    assert match_repository.find({"_id": match_a_id})[0].status == MatchStatus.open.value
    assert match_repository.find({"_id": match_b._id})[0].status == MatchStatus.open.value

    # 系列Aのみをselectで精算 → 系列Bには一切影響しない
    reply_service.reset()
    _set_group_request()
    request_info_service.params = {"to": str(match_a_id)}
    with patch(
        "application_service.graph_service.GraphService.create_users_point_plot_graph_url",
        return_value=(None, None),
    ):
        FinishMatchUseCase().select()

    settled_a = match_repository.find({"_id": match_a_id})[0]
    still_open_b = match_repository.find({"_id": match_b._id})[0]
    assert settled_a.status == MatchStatus.settled.value
    assert still_open_b.status == MatchStatus.open.value
    assert still_open_b.sum_scores  # 系列Bのスコアはそのまま残っている

    # 系列Aのレート(3)で精算されている(系列Bのレート7が誤って使われていない)
    a_price = next(iter(settled_a.sum_prices.values()))
    a_score = next(iter(settled_a.sum_scores.values()))
    assert a_price == a_score * 3 * 10

    # `_active_match`はもうopenが1件(系列B)だけなのでピッカーなしで直接表示する
    # (ReplyHanchansOfActiveMatchUseCaseはerr_messageがNoneならimage_urlの値を
    # 問わずadd_imageを呼ぶため、Noneではなくダミーの有効なURLを返す)
    reply_service.reset()
    _set_group_request()
    with patch(
        "application_service.graph_service.GraphService.create_users_point_plot_graph_url",
        return_value=("https://example.com/dummy.png", None),
    ):
        ReplyHanchansOfActiveMatchUseCase().execute()
    assert reply_service.texts[0].text == "途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。"

    # 系列Bも精算し、系列Bのレート(7)が使われていることを確認
    reply_service.reset()
    _set_group_request()
    request_info_service.params = {"to": str(match_b._id)}
    with patch(
        "application_service.graph_service.GraphService.create_users_point_plot_graph_url",
        return_value=(None, None),
    ):
        FinishMatchUseCase().select()

    settled_b = match_repository.find({"_id": match_b._id})[0]
    assert settled_b.status == MatchStatus.settled.value
    b_price = next(iter(settled_b.sum_prices.values()))
    b_score = next(iter(settled_b.sum_scores.values()))
    assert b_price == b_score * 7 * 10
