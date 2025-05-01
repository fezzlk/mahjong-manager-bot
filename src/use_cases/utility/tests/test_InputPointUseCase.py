from ApplicationService import (
    reply_service,
    request_info_service,
)
from use_cases.utility.InputPointUseCase import InputPointUseCase


def test_execute():
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.req_line_group_id = "test_group_id"
    request_info_service.req_line_user_id = "test_userid"

    # Act
    result = use_case.execute(text="1000")

    # Assert
    assert result[0] == "test_userid"
    assert result[1] == 1000


def test_execute_with_mention():
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.mention_line_ids = [
        "U0123456789abcdefghijklmnopqrstu1"]

    # Act
    result = use_case.execute(text="@test_user1 1000")

    # Assert
    assert result[0] == "U0123456789abcdefghijklmnopqrstu1"
    assert result[1] == 1000


def test_execute_multi_mentions():
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.mention_line_ids = [
        "U0123456789abcdefghijklmnopqrstu1",
        "U0123456789abcdefghijklmnopqrstu2",
    ]

    # Act
    result = use_case.execute(text="@dummy1 @dummy2 1000")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == "メンションは1回につき1人を指定するようにしてください。"
    assert result[0] is None
    assert result[1] is None


def test_execute_with_comma():
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.req_line_group_id = "test_group_id"
    request_info_service.req_line_user_id = "test_userid"

    # Act
    result = use_case.execute(text="1,000")

    # Assert
    assert result[0] == "test_userid"
    assert result[1] == 1000


def test_execute_minus():
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.req_line_group_id = "test_group_id"
    request_info_service.req_line_user_id = "test_userid"

    # Act
    result = use_case.execute(text="-1000")

    # Assert
    assert result[0] == "test_userid"
    assert result[1] == -1000


def test_execute_drop():
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.req_line_group_id = "test_group_id"
    request_info_service.req_line_user_id = "test_userid"

    # Act
    result = use_case.execute(text="-")

    # Assert
    assert result[0] == "test_userid"
    assert result[1] is None


def test_execute_drop_with_mention():
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.req_line_group_id = "test_group_id"
    request_info_service.req_line_user_id = "test_userid"
    request_info_service.mention_line_ids = [
        "U0123456789abcdefghijklmnopqrstu1"]

    # Act
    result = use_case.execute(text="@test -")

    # Assert
    assert result[0] == "U0123456789abcdefghijklmnopqrstu1"
    assert result[1] is None


def test_execute_not_int_point():
    # Arrange
    use_case = InputPointUseCase()

    # Act
    result = use_case.execute(text="hoge")

    # Assert
    assert result[0] is None
    assert result[1] is None


def test_execute_not_int_point_with_mention():
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.mention_line_ids = [
        "U0123456789abcdefghijklmnopqrstu1"]

    # Act
    result = use_case.execute(text="@test_user1 hoge")

    # Assert
    assert result[0] is None
    assert result[1] is None

