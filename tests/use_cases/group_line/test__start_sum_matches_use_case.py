from application_service import reply_service, request_info_service
from domain_model.entities.match import Match, MatchStatus
from line_models.event import Event
from repositories import match_repository, match_sum_session_repository
from use_cases.group_line.start_sum_matches_use_case import StartSumMatchesUseCase

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="_sum_matches",
)


def test_execute_no_matches():
    """settled対戦が1件もない場合は案内メッセージのみ返す。"""
    request_info_service.set_req_info(event=dummy_event)

    StartSumMatchesUseCase().execute()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "まだ対戦結果がありません。"


def test_execute_creates_session_and_shows_quick_reply():
    """settled対戦がある場合、セッションを作成し選択用Quick Replyを表示する。"""
    request_info_service.set_req_info(event=dummy_event)
    match = match_repository.create(
        Match(
            line_group_id=dummy_event.source.group_id,
            status=MatchStatus.settled.value,
            sum_prices_with_chip={"U1": 100},
        ),
    )

    StartSumMatchesUseCase().execute()

    session = match_sum_session_repository.find_active(dummy_event.source.group_id, dummy_event.source.user_id)
    assert session is not None
    assert session.selected_match_ids == []

    assert len(reply_service.texts) == 2
    quick_reply = reply_service.texts[1].quick_reply
    assert quick_reply is not None
    # 対戦1件 + 「合計を見る」ボタンで2項目
    assert len(quick_reply.items) == 2
    assert quick_reply.items[0].action.data == f"_sum_matches_toggle?to={match._id}"
    assert quick_reply.items[1].action.data == "_sum_matches_confirm"
