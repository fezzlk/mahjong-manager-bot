from application_service import (
    reply_service,
    request_info_service,
)
from use_cases.utility.input_point_use_case import InputPointUseCase


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result[0] が "test_userid" である / result[1] が 1000 である
    # reply_service: なし
    # DB操作: なし
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
    # 目的: test_execute_with_mention の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result[0] が "U0123456789abcdefghijklmnopqrstu1" である / result[1] が 1000 である
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.mention_line_ids = ["U0123456789abcdefghijklmnopqrstu1"]

    # Act
    result = use_case.execute(text="@test_user1 1000")

    # Assert
    assert result[0] == "U0123456789abcdefghijklmnopqrstu1"
    assert result[1] == 1000


def test_execute_multi_mentions() -> None:
    """Test the execute method when multiple mentions are included in the input text."""
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
    assert (
        reply_service.texts[0].text
        == "メンションは1回につき1人を指定するようにしてください。"
    )
    assert result[0] is None
    assert result[1] is None


def test_execute_with_comma() -> None:
    """Test the execute method when the input text includes a comma in the point value."""
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.req_line_group_id = "test_group_id"
    request_info_service.req_line_user_id = "test_userid"

    # Act
    result = use_case.execute(text="1,000")

    # Assert
    assert result[0] == "test_userid"
    assert result[1] == 1000


def test_execute_minus() -> None:
    """Test the execute method when the input text is a negative integer point."""
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.req_line_group_id = "test_group_id"
    request_info_service.req_line_user_id = "test_userid"

    # Act
    result = use_case.execute(text="-1000")

    # Assert
    assert result[0] == "test_userid"
    assert result[1] == -1000


def test_execute_drop() -> None:
    """Test the execute method when the input text is a drop symbol."""
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.req_line_group_id = "test_group_id"
    request_info_service.req_line_user_id = "test_userid"

    # Act
    result = use_case.execute(text="-")

    # Assert
    assert result[0] == "test_userid"
    assert result[1] is None


def test_execute_drop_with_mention() -> None:
    """Test the execute method when the input text includes a mention and a drop symbol."""
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.req_line_group_id = "test_group_id"
    request_info_service.req_line_user_id = "test_userid"
    request_info_service.mention_line_ids = ["U0123456789abcdefghijklmnopqrstu1"]

    # Act
    result = use_case.execute(text="@test -")

    # Assert
    assert result[0] == "U0123456789abcdefghijklmnopqrstu1"
    assert result[1] is None


def test_execute_not_int_point() -> None:
    """Test the execute method when the input text is not an integer point."""
    # Arrange
    use_case = InputPointUseCase()

    # Act
    result = use_case.execute(text="hoge")

    # Assert
    assert result[0] is None
    assert result[1] is None


def test_execute_not_int_point_with_mention() -> None:
    """Test the execute method when the input text is not an integer point.

    and includes a mention.
    """
    # Arrange
    use_case = InputPointUseCase()
    request_info_service.mention_line_ids = ["U0123456789abcdefghijklmnopqrstu1"]

    # Act
    result = use_case.execute(text="@test_user1 hoge")

    # Assert
    assert result[0] is None
    assert result[1] is None
