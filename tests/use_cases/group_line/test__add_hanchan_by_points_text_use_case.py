from application_service import reply_service, request_info_service
from domain_model.entities.group import Group
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.user import User
from line_models.event import Event
from repositories import group_repository, hanchan_repository, user_repository
from use_cases.group_line.add_hanchan_by_points_text_use_case import (
    AddHanchanByPointsTextUseCase,
)


dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)


def test_execute_when_group_not_found():
    # 目的: test_execute_when_group_not_found の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / (
    # reply_service: texts
    # DB操作: なし
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = AddHanchanByPointsTextUseCase()

    # Act
    use_case.execute("Alice:25000")

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "グループが登録されていません。招待し直してください。"
    )


def test_execute_with_insufficient_points_creates_hanchan():
    # 目的: test_execute_with_insufficient_points_creates_hanchan の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "4人分の点数を入力してください" である / hanchans の件数が 1 件 / hanchans[0] が Hanchan 型
    # reply_service: texts
    # DB操作: group_repository.create(group); user_repository.create(user); hanchans = hanchan_repository.find({"line_group_id": group.line_group_id})
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = AddHanchanByPointsTextUseCase()

    group = Group(line_group_id=dummy_event.source.group_id)
    group_repository.create(group)

    users = [
        User(line_user_id="U1", line_user_name="Alice"),
        User(line_user_id="U2", line_user_name="Bob"),
        User(line_user_id="U3", line_user_name="Carol"),
    ]
    for user in users:
        user_repository.create(user)

    # Act
    use_case.execute("Alice:25000\nBob:25000\nCarol:25000")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "4人分の点数を入力してください"

    hanchans = hanchan_repository.find({"line_group_id": group.line_group_id})
    assert len(hanchans) == 1
    assert isinstance(hanchans[0], Hanchan)
