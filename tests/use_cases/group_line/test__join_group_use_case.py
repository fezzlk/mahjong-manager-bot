import pytest
from dummies import (
    generate_dummy_join_event,
)
from linebot.v3.messaging import (
    TemplateMessage,
    TextMessage,
)
from linebot.v3.messaging.exceptions import ApiException

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.match import Match, MatchStatus
from repositories import group_repository, match_repository
from use_cases.group_line.join_group_use_case import JoinGroupUseCase

_MODULE = "use_cases.group_line.join_group_use_case"


def _make_dummy_summary(group_name="テストグループ", picture_url="http://example.com/g.jpg"):
    from unittest.mock import MagicMock
    summary = MagicMock()
    summary.group_name = group_name
    summary.picture_url = picture_url
    return summary


def test_fail_no_line_group_id():
    use_case = JoinGroupUseCase()

    with pytest.raises(
        ValueError,
        match="登録する line_group_id が未指定です。",
    ):
        use_case.execute()


def test_execute(mocker):
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)
    mocker.patch(
        f"{_MODULE}.line_bot_api.get_group_summary",
        return_value=_make_dummy_summary(),
    )

    JoinGroupUseCase().execute()

    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_event.source.group_id
    assert result[0].mode == "wait"
    assert result[0].group_name == "テストグループ"
    assert len(reply_service.texts) == 3
    assert isinstance(reply_service.texts[0], TextMessage)
    assert isinstance(reply_service.texts[1], TextMessage)
    assert isinstance(reply_service.texts[2], TextMessage)
    assert (
        reply_service.texts[0].text
        == "麻雀の成績管理Botです。参加者は友達登録してください。"
    )
    assert (
        reply_service.texts[1].text
        == "1半荘が終了したら下のメニューの「結果を入力」を押し、それぞれ素点を入力して下さい。"
    )
    assert (
        reply_service.texts[2].text == "レートや点数計算方法は「設定」で変更可能です。"
    )
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateMessage)
    assert reply_service.buttons[0].quick_reply is None


def test_execute_with_existing_open_match_adds_new_match_quick_reply(mocker):
    """再招待等でopen対戦が既に存在する状態でjoinした場合も「新しい対戦を始める」導線が付与される。"""
    dummy_event = generate_dummy_join_event()
    match_repository.create(
        Match(
            line_group_id=dummy_event.source.group_id,
            status=MatchStatus.open.value,
            _id=1,
        ),
    )
    request_info_service.set_req_info(event=dummy_event)
    mocker.patch(
        f"{_MODULE}.line_bot_api.get_group_summary",
        return_value=_make_dummy_summary(),
    )

    JoinGroupUseCase().execute()

    quick_reply = reply_service.buttons[0].quick_reply
    assert quick_reply is not None
    assert quick_reply.items[0].action.data == "_new_match"


def test_execute_group_summary_api_failure(mocker):
    """get_group_summary が失敗してもJoin処理自体は正常完了する。"""
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)
    mocker.patch(
        f"{_MODULE}.line_bot_api.get_group_summary",
        side_effect=ApiException(status=403, reason="Forbidden"),
    )

    JoinGroupUseCase().execute()

    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_event.source.group_id
    assert result[0].group_name is None
    assert len(reply_service.texts) == 3
