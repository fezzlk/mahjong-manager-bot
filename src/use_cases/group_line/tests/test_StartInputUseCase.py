from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.Group import Group, GroupMode
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from line_models.Event import Event
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
)
from use_cases.group_line.StartInputUseCase import StartInputUseCase

dummy_groups = [
    Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    ),
    Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
    ),
]

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="_input",
)

def test_execute_no_group():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    group_repository.create(dummy_groups[1])

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "トークルームが登録されていません。招待し直してください。"


def test_execute_input_mode():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    dummy_groups1 = [
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.input.value,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
        ),
    ]
    for dummy_group in dummy_groups1:
        group_repository.create(dummy_group)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "すでに入力モードです。"


def test_execute_new_match():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    for dummy_group in dummy_groups:
        group_repository.create(dummy_group)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "第1回戦お疲れ様です。各自点数を入力してください。\n（同点の場合は上家が高くなるように数点追加してください）"
    groups = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})
    assert len(groups) == 1
    assert groups[0].active_match_id is not None
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is not None
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 1


def test_execute_new_hanchan():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    dummy_groups2 = [
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            active_match_id=1,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
        ),
    ]
    for dummy_group in dummy_groups2:
        group_repository.create(dummy_group)
    match_repository.create(Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    ))

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "第1回戦お疲れ様です。各自点数を入力してください。\n（同点の場合は上家が高くなるように数点追加してください）"
    groups = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})
    assert len(groups) == 1
    assert groups[0].active_match_id is not None
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is not None
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 1


def test_execute_with_hanchan():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    dummy_groups2 = [
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            active_match_id=1,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
        ),
    ]
    for dummy_group in dummy_groups2:
        group_repository.create(dummy_group)
    match_repository.create(Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=1,
    ))
    hanchan_repository.create(Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        _id=1,
    ))

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "第1回戦お疲れ様です。各自点数を入力してください。\n（同点の場合は上家が高くなるように数点追加してください）"
    groups = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})
    assert len(groups) == 1
    assert groups[0].active_match_id is not None
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is not None
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 1

