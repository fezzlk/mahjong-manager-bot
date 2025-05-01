import pytest

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
from use_cases.group_line.DropHanchanByIndexUseCase import DropHanchanByIndexUseCase

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    active_match_id=1,
    _id=1,
)

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        _id=1,
    ),
]
dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=2,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
        _id=1,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=2,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
        _id=2,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=2,
        _id=3,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=2,
        _id=4,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=0,
        _id=5,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=999,
        status=2,
        _id=6,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        status=2,
        _id=7,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
    ),
]


def test_execute():
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("2")

    # Assert
    hanchans = hanchan_repository.find({"_id": 2})
    assert len(hanchans) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "現在の対戦の第2半荘の結果を削除しました。"


def test_execute_ignore_other_hanchans():
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("4")

    # Assert
    hanchans = hanchan_repository.find({"_id": 7})
    assert len(hanchans) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "現在の対戦の第4半荘の結果を削除しました。"


def test_execute_arg_int():
    with pytest.raises(BaseException):
        # Arrange
        use_case = DropHanchanByIndexUseCase()
        request_info_service.set_req_info(event=dummy_event)
        group_repository.create(dummy_group)
        match_repository.create(dummy_matches[0])
        for dummy_hanchan in dummy_hanchans:
            hanchan_repository.create(dummy_hanchan)

        # Act
        use_case.execute(1)

    # Assert
    records_in_db = hanchan_repository.find()
    assert len(records_in_db) == 6


def test_execute_no_arg():
    with pytest.raises(BaseException):
        # Arrange
        use_case = DropHanchanByIndexUseCase()
        request_info_service.set_req_info(event=dummy_event)
        group_repository.create(dummy_group)
        match_repository.create(dummy_matches[0])
        for dummy_hanchan in dummy_hanchans:
            hanchan_repository.create(dummy_hanchan)

        # Act
        use_case.execute(1)

    # Assert
    records_in_db = hanchan_repository.find()
    assert len(records_in_db) == 6


def test_execute_arg_no_digit():
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("test")

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "引数は整数で指定してください。"


def test_execute_no_group():
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("1")

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "トークルームが登録されていません。招待し直してください。"


def test_execute_no_match():
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    no_match_group = Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        mode=GroupMode.input.value,
        _id=1,
    )
    group_repository.create(no_match_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("1")

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "現在進行中の対戦がありません。"


def test_execute_fail_get_active_match():
    with pytest.raises(BaseException):
        # Arrange
        use_case = DropHanchanByIndexUseCase()
        request_info_service.set_req_info(event=dummy_event)
        group_repository.create(dummy_group)
        for dummy_hanchan in dummy_hanchans:
            hanchan_repository.create(dummy_hanchan)

        # Act
        use_case.execute("1")

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 0


@pytest.fixture(params=["0", "5"])
def text_case1(request):
    return request.param


def test_execute_out_of_index(text_case1):
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute(text_case1)

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == f"このトークルームには全4回までしか登録されていないため第{text_case1}回はありません。"
