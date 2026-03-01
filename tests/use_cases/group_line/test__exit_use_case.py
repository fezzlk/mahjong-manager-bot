from linebot.models import TextSendMessage

from application_service import (
        reply_service,
        request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from line_models.event import Event
from repositories import (
        group_repository,
        hanchan_repository,
        match_repository,
)
from use_cases.group_line.exit_use_case import ExitUseCase

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    _id=1,
)

dummy_match = Match(
    line_group_id=dummy_group.line_group_id,
    _id=1,
)

dummy_hanchan = Hanchan(
    line_group_id=dummy_group.line_group_id,
    match_id=1,
    _id=1,
)

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="_exit",
)


def test_fail_no_group():
    # 目的: test_fail_no_group の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "グループが登録されていません。招待し直してください。" である
    # reply_service: texts
    # DB操作: なし
        # Arrange
        use_case = ExitUseCase()
        request_info_service.set_req_info(event=dummy_event)

        # Act
        use_case.execute()

        # Assert
        assert len(reply_service.texts) == 1
        assert reply_service.texts[0].text == "グループが登録されていません。招待し直してください。"


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result の件数が 1 件 / result[0].line_group_id が dummy_group.line_group_id である / result[0].mode が "wait" である / reply_service.texts の件数が 1 件 / reply_service.texts[0] が TextSendMessage 型 / reply_service.texts[0].text が "始める時は「_start」と入力してください。" である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); result = group_repository.find()
    # Arrange
    use_case = ExitUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)

    # Act
    use_case.execute()

    # Assert
    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_group.line_group_id
    assert result[0].mode == "wait"
    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert reply_service.texts[0].text == "始める時は「_start」と入力してください。"


def test_execute_with_active_hanchan():
    # 目的: test_execute_with_active_hanchan の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result の件数が 1 件 / result[0].line_group_id が dummy_group.line_group_id である / result[0].mode が "wait" である / result[0].active_match_id が dummy_match._id である / reply_service.texts の件数が 1 件 / reply_service.texts[0] が TextSendMessage 型 / reply_service.texts[0].text が "始める時は「_start」と入力してください。" である / matches の件数が 1 件 / matches[0].active_hanchan_id is None / matches[0].status が dummy_match.status である / hanchans の件数が 0 件
    # reply_service: texts
    # DB操作: hanchan_repository.create(dummy_hanchan); match_repository.create(dummy_match); group_repository.create(dummy_group); result = group_repository.find(); matches = match_repository.find(); hanchans = hanchan_repository.find()
    # Arrange
    use_case = ExitUseCase()
    request_info_service.set_req_info(event=dummy_event)
    hanchan_repository.create(dummy_hanchan)
    dummy_match.active_hanchan_id = dummy_hanchan._id
    match_repository.create(dummy_match)
    dummy_group.active_match_id = dummy_match._id
    group_repository.create(dummy_group)

    # Act
    use_case.execute()

    # Assert
    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_group.line_group_id
    assert result[0].mode == "wait"
    assert result[0].active_match_id == dummy_match._id
    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert reply_service.texts[0].text == "始める時は「_start」と入力してください。"
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is None
    assert matches[0].is_deleted == dummy_match.is_deleted
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 0


def test_execute_without_active_hanchan():
    # 目的: test_execute_without_active_hanchan の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result の件数が 1 件 / result[0].line_group_id が dummy_group.line_group_id である / result[0].mode が "wait" である / result[0].active_match_id が dummy_match._id である / reply_service.texts の件数が 1 件 / reply_service.texts[0] が TextSendMessage 型 / reply_service.texts[0].text が "始める時は「_start」と入力してください。" である / matches の件数が 1 件 / matches[0].active_hanchan_id is None / matches[0].status が dummy_match.status である / hanchans の件数が 0 件
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); result = group_repository.find(); matches = match_repository.find(); hanchans = hanchan_repository.find()
    # Arrange
    use_case = ExitUseCase()
    request_info_service.set_req_info(event=dummy_event)
    match_repository.create(dummy_match)
    dummy_group.active_match_id = dummy_match._id
    group_repository.create(dummy_group)

    # Act
    use_case.execute()

    # Assert
    result = group_repository.find()
    assert len(result) == 1
    assert result[0].line_group_id == dummy_group.line_group_id
    assert result[0].mode == "wait"
    assert result[0].active_match_id == dummy_match._id
    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert reply_service.texts[0].text == "始める時は「_start」と入力してください。"
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is None
    assert matches[0].is_deleted == dummy_match.is_deleted
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 0
