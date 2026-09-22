from application_service import reply_service, request_info_service
from domain_model.entities.match import Match, MatchStatus
from domain_model.entities.match_sum_session import MatchSumSession
from line_models.event import Event
from repositories import match_repository, match_sum_session_repository
from use_cases.group_line.confirm_sum_matches_use_case import ConfirmSumMatchesUseCase

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)


def test_execute_times_out_without_session():
    """セッションが存在しない場合はタイムアウトメッセージが返る。"""
    request_info_service.set_req_info(event=dummy_event)

    ConfirmSumMatchesUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "タイムアウト" in reply_service.texts[0].text


def test_execute_reprompts_when_nothing_selected():
    """選択が0件のまま確定しようとすると再度選択UIを表示する。"""
    request_info_service.set_req_info(event=dummy_event)
    match_repository.create(
        Match(line_group_id=dummy_event.source.group_id, status=MatchStatus.settled.value),
    )
    match_sum_session_repository.create(
        MatchSumSession(
            line_group_id=dummy_event.source.group_id,
            requester_line_id=dummy_event.source.user_id,
            selected_match_ids=[],
        ),
    )

    ConfirmSumMatchesUseCase().execute()

    assert reply_service.texts[0].text == "対戦を選んでください。"
    assert reply_service.texts[1].quick_reply is not None


def test_execute_shows_combined_total_and_clears_session():
    """選択した複数対戦の合計金額をプレイヤーごとに合算して表示し、セッションを削除する。"""
    request_info_service.set_req_info(event=dummy_event)
    match1 = match_repository.create(
        Match(
            line_group_id=dummy_event.source.group_id,
            status=MatchStatus.settled.value,
            sum_prices_with_chip={"U1": 1000, "U2": -1000},
        ),
    )
    match2 = match_repository.create(
        Match(
            line_group_id=dummy_event.source.group_id,
            status=MatchStatus.settled.value,
            sum_prices_with_chip={"U1": -500, "U2": 500},
        ),
    )
    match_sum_session_repository.create(
        MatchSumSession(
            line_group_id=dummy_event.source.group_id,
            requester_line_id=dummy_event.source.user_id,
            selected_match_ids=[str(match1._id), str(match2._id)],
        ),
    )

    ConfirmSumMatchesUseCase().execute()

    assert len(reply_service.texts) == 1
    text = reply_service.texts[0].text
    assert "選択した2件の対戦の合計" in text
    assert "U1" not in text  # 友達未登録の表示名に変換される
    assert "友達未登録: +500円" in text
    assert "友達未登録: -500円" in text

    assert match_sum_session_repository.find_active_by_group_id(dummy_event.source.group_id) is None
