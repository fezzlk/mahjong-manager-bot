import pytest
from dummies import (
    generate_dummy_join_event,
)
from linebot.v3.messaging import (
    TemplateMessage,
    TextMessage,
)

from application_service import (
    reply_service,
    request_info_service,
)
from repositories import group_repository
from use_cases.group_line.join_group_use_case import JoinGroupUseCase


def test_fail_no_line_group_id():
    # 目的: test_fail_no_line_group_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: 明示的なassertなし（期待される挙動を説明）
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = JoinGroupUseCase()

    # Act
    with pytest.raises(
        ValueError,
        match="登録する line_group_id が未指定です。",
    ):
        use_case.execute()

    # Assert


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result の件数が 1 件 / result[0].line_group_id が dummy_event.source.group_id である / result[0].mode が "wait" である / reply_service.texts の件数が 3 件 / reply_service.texts[0] が TextSendMessage 型 / reply_service.texts[1] が TextSendMessage 型 / reply_service.texts[2] が TextSendMessage 型 / ( / ( / ( / reply_service.buttons の件数が 1 件 / reply_service.buttons[0] が TemplateSendMessage 型
    # reply_service: buttons, texts
    # DB操作: result = group_repository.find()
    # Arrange
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)

    use_case = JoinGroupUseCase()

    # Act
    use_case.execute()

    # Assert
    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_event.source.group_id
    assert result[0].mode == "wait"
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
