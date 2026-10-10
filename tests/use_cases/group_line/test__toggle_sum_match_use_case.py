from application_service import reply_service, request_info_service
from domain_model.entities.match import Match, MatchStatus
from domain_model.entities.match_sum_session import MatchSumSession
from line_models.event import Event
from repositories import match_repository, match_sum_session_repository
from use_cases.group_line.toggle_sum_match_use_case import ToggleSumMatchUseCase

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)


def test_execute_times_out_without_session():
    """セッションが存在しない(期限切れ含む)場合はタイムアウトメッセージが返る。"""
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"to": "644c838186bbd9e20a91b785"}

    ToggleSumMatchUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "タイムアウト" in reply_service.texts[0].text


def test_execute_toggles_selection_on_and_off():
    """トグルで選択/解除でき、再表示のラベルにチェックマークが反映される。"""
    request_info_service.set_req_info(event=dummy_event)
    match = match_repository.create(
        Match(
            line_group_id=dummy_event.source.group_id,
            status=MatchStatus.settled.value,
            sum_prices_with_chip={"U1": 100},
        ),
    )
    match_sum_session_repository.create(
        MatchSumSession(
            line_group_id=dummy_event.source.group_id,
            requester_line_id=dummy_event.source.user_id,
            selected_match_ids=[],
        ),
    )
    request_info_service.params = {"to": str(match._id)}

    # 1回目のトグル: 選択される
    ToggleSumMatchUseCase().execute()
    session = match_sum_session_repository.find_active(dummy_event.source.group_id, dummy_event.source.user_id)
    assert session.selected_match_ids == [str(match._id)]
    quick_reply = reply_service.texts[-1].quick_reply
    assert quick_reply.items[0].action.label.startswith("✓")

    # 2回目のトグル: 選択解除される
    ToggleSumMatchUseCase().execute()
    session = match_sum_session_repository.find_active(dummy_event.source.group_id, dummy_event.source.user_id)
    assert session.selected_match_ids == []
    quick_reply = reply_service.texts[-1].quick_reply
    assert not quick_reply.items[0].action.label.startswith("✓")


def test_toggle_by_other_member_does_not_touch_requester_session():
    """同じグループの別メンバーの操作は、開始した本人のセッションに影響しない。"""
    request_info_service.set_req_info(event=dummy_event)
    match = match_repository.create(
        Match(
            line_group_id=dummy_event.source.group_id,
            status=MatchStatus.settled.value,
            sum_prices_with_chip={"U1": 100},
        ),
    )
    match_sum_session_repository.create(
        MatchSumSession(
            line_group_id=dummy_event.source.group_id,
            requester_line_id=dummy_event.source.user_id,
            selected_match_ids=[],
        ),
    )

    # 別メンバーがトグルしても、その人のセッションは無いのでタイムアウト扱い
    request_info_service.req_line_user_id = "U_other_member"
    request_info_service.params = {"to": str(match._id)}
    ToggleSumMatchUseCase().execute()

    assert reply_service.texts[-1].text.startswith("タイムアウトしました")
    session = match_sum_session_repository.find_active(dummy_event.source.group_id, dummy_event.source.user_id)
    assert session.selected_match_ids == []
