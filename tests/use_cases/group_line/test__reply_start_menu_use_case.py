from linebot.v3.messaging import TemplateMessage

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.match import Match, MatchStatus
from repositories import match_repository
from use_cases.group_line.reply_start_menu_use_case import ReplyStartMenuUseCase

LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.buttons の件数が 1 件 / reply_service.buttons[0] が TemplateSendMessage 型
    # reply_service: buttons
    # DB操作: なし
    # Arrange
    use_case = ReplyStartMenuUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.buttons) == 1
    assert isinstance(reply_service.buttons[0], TemplateMessage)


def test_execute_with_open_match_adds_new_match_quick_reply():
    """進行中(open)の対戦が1件以上あるとき、「新しい対戦を始める」導線が付与される。"""
    match_repository.create(
        Match(line_group_id=LINE_GROUP_ID, status=MatchStatus.open.value, _id=1),
    )
    request_info_service.req_line_group_id = LINE_GROUP_ID

    use_case = ReplyStartMenuUseCase()
    use_case.execute()

    quick_reply = reply_service.buttons[0].quick_reply
    assert quick_reply is not None
    assert quick_reply.items[0].action.data == "_new_match"


def test_execute_without_open_match_has_no_quick_reply():
    """進行中(open)の対戦が0件のとき、「新しい対戦を始める」導線は付与されない。"""
    request_info_service.req_line_group_id = LINE_GROUP_ID

    use_case = ReplyStartMenuUseCase()
    use_case.execute()

    assert reply_service.buttons[0].quick_reply is None


def test_execute_with_settled_match_only_has_no_quick_reply():
    """精算済み(settled)の対戦しかないときは「新しい対戦を始める」導線は付与されない。"""
    match_repository.create(
        Match(line_group_id=LINE_GROUP_ID, status=MatchStatus.settled.value, _id=1),
    )
    request_info_service.req_line_group_id = LINE_GROUP_ID

    use_case = ReplyStartMenuUseCase()
    use_case.execute()

    assert reply_service.buttons[0].quick_reply is None
