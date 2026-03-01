from datetime import datetime
from typing import Dict

import pytest
from bson.objectid import ObjectId

import env_var
from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from domain_model.entities.user import User, UserMode
from domain_model.entities.user_match import UserMatch
from repositories import (
    hanchan_repository,
    match_repository,
    user_match_repository,
    user_repository,
)
from use_cases.personal_line.reply_history_use_case import ReplyHistoryUseCase

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user1",
)

dummy_match = Match(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    _id=ObjectId("644c838186bbd9e20a91b783"),
)

dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 40000,
            "U0123456789abcdefghijklmnopqrstu2": 30000,
            "U0123456789abcdefghijklmnopqrstu3": 20000,
            "U0123456789abcdefghijklmnopqrstu4": 10000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 50,
            "U0123456789abcdefghijklmnopqrstu2": 10,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu4": -40,
        },
        match_id=ObjectId("644c838186bbd9e20a91b783"),
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 40000,
            "U0123456789abcdefghijklmnopqrstu2": 30000,
            "U0123456789abcdefghijklmnopqrstu3": 20000,
            "U0123456789abcdefghijklmnopqrstu4": 10000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 50,
            "U0123456789abcdefghijklmnopqrstu2": 10,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu4": -40,
        },
        match_id=ObjectId("644c838186bbd9e20a91b783"),
    ),
]


def test_execute_no_user():
    # 目的: test_execute_no_user の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / ( / (
    # reply_service: texts
    # DB操作: user_repository.create(dummy_user)
    # Arrange
    user_repository.create(dummy_user)

    request_info_service.req_line_user_id = "unknown"
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert (
        reply_service.texts[0].text
        == "ユーザーが登録されていません。友達追加してください。"
    )
    assert (
        reply_service.texts[1].text
        == "既に友達の場合は一度ブロックして、ブロック解除を行ってください。"
    )


@pytest.fixture(
    params=[
        {"from": "x"},
        {"to": "x"},
        {"from": "x", "to": "20220101"},
        {"from": "20220101", "to": "x"},
        {"from": "x", "to": "x"},
    ],
)
def case1(request) -> Dict[str, str]:
    return request.param


def test_execute_invalid_range_format(case1):
    # 目的: test_execute_invalid_range_format の挙動を検証する。
    # 入力: case1
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / reply_service.texts[0].text が "日付は以下のフォーマットで入力してください。" である / (
    # reply_service: texts
    # DB操作: user_repository.create(dummy_user)
    # Arrange
    user_repository.create(dummy_user)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    request_info_service.params = case1
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == "日付は以下のフォーマットで入力してください。"
    assert (
        reply_service.texts[1].text
        == "[日付の入力方法]\n\nYYYY年MM月DD日\n→ YYYYMMDD\n\n20YY年MM月DD日\n→ YYMMDD\n\n今年MM月DD日\n→ MMDD\n\n今月DD日\n→ DD"
    )


def test_execute_not_match():
    # 目的: test_execute_not_match の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "対局履歴がありません。" である
    # reply_service: texts
    # DB操作: user_repository.create(dummy_user)
    # Arrange
    user_repository.create(dummy_user)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "対局履歴がありません。"


def test_fail_get_hanchans():
    # 目的: test_fail_get_hanchans の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: 明示的なassertなし（期待される挙動を説明）
    # reply_service: なし
    # DB操作: user = user_repository.create(dummy_user); match_repository.create(dummy_match); user_match_repository.create(dummy_user_match)
    # Arrange
    user = user_repository.create(dummy_user)
    match_repository.create(dummy_match)

    dummy_user_match = UserMatch(
        user_id=user._id,
        match_id=dummy_match._id,
    )
    user_match_repository.create(dummy_user_match)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    use_case = ReplyHistoryUseCase()

    # Act
    with pytest.raises(
        ValueError,
        match="半荘情報を取得できませんでした。",
    ):
        use_case.execute()

    # Assert


def test_execute(mocker):
    # 目的: test_execute の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 1 件
    # reply_service: images
    # DB操作: user = user_repository.create(dummy_user); match = match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_match_repository.create(dummy_user_match)
    # Arrange
    import matplotlib.pyplot as plt  # noqa: PLC0415

    fig = plt.figure()
    mocker.patch.object(
        plt,
        "figure",
        return_value=fig,
    )
    mock_fig = mocker.patch.object(
        fig,
        "savefig",
        return_value=None,
    )

    user = user_repository.create(dummy_user)
    match = match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    dummy_user_match = UserMatch(
        user_id=user._id,
        match_id=match._id,
    )
    user_match_repository.create(dummy_user_match)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    mock_fig.assert_called_once()
    assert len(reply_service.images) == 1


@pytest.fixture(
    params=[
        ({"from": "20230101"}, "範囲指定: 2023年01月01日0時から"),
        ({"to": "20241231"}, "範囲指定: 2024年12月31日0時まで"),
        (
            {"from": "20230101", "to": "20241231"},
            "範囲指定: 2023年01月01日0時から2024年12月31日0時まで",
        ),
    ],
)
def case2(request) -> Dict[str, str]:
    return request.param


def test_execute_with_range(mocker, case2):
    # 目的: test_execute_with_range の挙動を検証する。
    # 入力: mocker, case2
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 1 件 / reply_service.texts の件数が 3 件 / reply_service.texts[0].text が case2[1] である
    # reply_service: images, texts
    # DB操作: user = user_repository.create(dummy_user); match = match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_match_repository.create(dummy_user_match)
    # Arrange
    import matplotlib.pyplot as plt  # noqa: PLC0415

    fig = plt.figure()
    mocker.patch.object(
        plt,
        "figure",
        return_value=fig,
    )
    mock_fig = mocker.patch.object(
        fig,
        "savefig",
        return_value=None,
    )
    user = user_repository.create(dummy_user)
    match = match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    dummy_user_match = UserMatch(
        user_id=user._id,
        match_id=match._id,
        created_at=datetime(2023, 1, 1, 1, 1, 2),
        _id=1,
    )
    user_match_repository.create(dummy_user_match)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    request_info_service.params = case2[0]
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    mock_fig.assert_called_once()
    assert len(reply_service.images) == 1
    assert len(reply_service.texts) == 3
    assert reply_service.texts[0].text == case2[1]


def test_fail_file_upload(mocker):
    # 目的: test_fail_file_upload の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 0 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "システムエラーが発生しました。" である
    # reply_service: images, texts
    # DB操作: user = user_repository.create(dummy_user); match = match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_match_repository.create(dummy_user_match)
    # Arrange
    import matplotlib.pyplot as plt  # noqa: PLC0415

    fig = plt.figure()
    mock = mocker.patch.object(
        reply_service,
        "push_a_message",
    )
    mocker.patch.object(
        plt,
        "figure",
        return_value=fig,
    )
    mocker.patch.object(
        fig,
        "savefig",
        side_effect=FileNotFoundError(),
    )

    user = user_repository.create(dummy_user)
    match = match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    dummy_user_match = UserMatch(
        user_id=user._id,
        match_id=match._id,
    )
    user_match_repository.create(dummy_user_match)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.images) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "システムエラーが発生しました。"
    mock.assert_called_once_with(
        to=env_var.SERVER_ADMIN_LINE_USER_ID,
        message="対戦履歴の画像アップロードに失敗しました\n送信者: U0123456789abcdefghijklmnopqrstu1",
    )
