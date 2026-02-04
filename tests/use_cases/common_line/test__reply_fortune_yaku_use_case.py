from application_service import (
    message_service,
    reply_service,
    request_info_service,
)
from domain_model.entities.user import User
from line_models.event import Event
from repositories import user_repository
from use_cases.common_line.reply_fortune_yaku_use_case import ReplyFortuneYakuUseCase

dummy_event = Event(
    type="join",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
)


def test_execute(mocker):
    # 目的: test_execute の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "testさんの今日のラッキー役は「リーチ」です。" である
    # reply_service: texts
    # DB操作: user_repository.create(User("U0123456789abcdefghijklmnopqrstu1", line_user_name="test"))
    # Arrange
    mocker.patch.object(
        message_service,
        "get_random_yaku",
        return_value="リーチ",
    )
    user_repository.create(User("U0123456789abcdefghijklmnopqrstu1", line_user_name="test"))
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyFortuneYakuUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "testさんの今日のラッキー役は「リーチ」です。"


def test_execute_no_user():
    # 目的: test_execute_no_user の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "ユーザーが登録されていません。友達追加してください。" である
    # reply_service: texts
    # DB操作: なし
    # Arrange
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyFortuneYakuUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "ユーザーが登録されていません。友達追加してください。"
