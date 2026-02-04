from datetime import datetime

import matplotlib.pyplot as plt

import env_var
from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from domain_model.entities.user import User
from line_models.event import Event
from repositories import (
    hanchan_repository,
    match_repository,
    user_repository,
)
from use_cases.group_line.create_match_detail_graph_use_case import (
    CreateMatchDetailGraphUseCase,
)

dummy_matches = [
    Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        created_at=datetime(2010, 1, 1, 1, 1, 1),
        sum_prices_with_chip={
            "U0123456789abcdefghijklmnopqrstu1": 1000,
            "U0123456789abcdefghijklmnopqrstu2": 1800,
            "U0123456789abcdefghijklmnopqrstu3": -1800,
            "U0123456789abcdefghijklmnopqrstu4": -400,
            "U0123456789abcdefghijklmnopqrstu5": -300,
            "dummy": -300,
        },
    ),
    Match(
        _id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        sum_prices_with_chip={
            "U0123456789abcdefghijklmnopqrstu1": 1000,
            "U0123456789abcdefghijklmnopqrstu2": 1800,
            "U0123456789abcdefghijklmnopqrstu3": -1800,
            "U0123456789abcdefghijklmnopqrstu4": -400,
            "U0123456789abcdefghijklmnopqrstu5": -300,
            "dummy": -300,
        },
    ),
    Match(
        _id=3,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=0,
        created_at=datetime(2010, 1, 1, 1, 1, 3),
    ),
    Match(
        _id=4,
        line_group_id="dummy",
        status=2,
        created_at=datetime(2010, 1, 1, 1, 1, 4),
    ),
]

dummy_hanchans = [
    Hanchan(
        _id=1,
        match_id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=0,
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu4": -10,
        },
    ),
    Hanchan(
        _id=2,
        match_id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu4": -10,
        },
    ),
    Hanchan(
        _id=3,
        match_id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu5": -10,
        },
    ),
    Hanchan(
        _id=4,
        match_id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "dummy": -10,
        },
    ),
    Hanchan(
        _id=5,
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu4": -10,
        },
    ),
]

dummy_users = [
    User(
        _id=1,
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        line_user_name="test_user1",
    ),
    User(
        _id=2,
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        line_user_name="test_user2",
    ),
    User(
        _id=3,
        line_user_id="U0123456789abcdefghijklmnopqrstu3",
        line_user_name="test_user3",
    ),
    User(
        _id=4,
        line_user_id="U0123456789abcdefghijklmnopqrstu4",
        line_user_name="test_user4",
    ),
    User(
        _id=5,
        line_user_id="U0123456789abcdefghijklmnopqrstu5",
        line_user_name="test_user5",
    ),
]

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="_graph",
)


def test_execute(mocker):
    # 目的: test_execute の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result が f"{env_var.SERVER_URL}uploads/match_detail/1.png" である
    # reply_service: なし
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_repository.create(dummy_user)
    # Arrange
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        "subplots",
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        "savefig",
    )

    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = CreateMatchDetailGraphUseCase()

    # Act
    result = use_case.execute(1)

    # Assert
    assert result == f"{env_var.SERVER_URL}uploads/match_detail/1.png"


def test_execute_fail_savefig(mocker):
    # 目的: test_execute_fail_savefig の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 0 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "システムエラーが発生しました。" である
    # reply_service: images, texts
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_repository.create(dummy_user)
    # Arrange
    mock = mocker.patch.object(
        reply_service,
        "push_a_message",
    )
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        "subplots",
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        "savefig",
        side_effect=FileNotFoundError(),
    )

    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = CreateMatchDetailGraphUseCase()

    # Act
    use_case.execute(1)

    # Assert
    assert len(reply_service.images) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "システムエラーが発生しました。"
    mock.assert_called_once_with(
        to=env_var.SERVER_ADMIN_LINE_USER_ID,
        message="対戦履歴の画像アップロードに失敗しました\n送信者: test_user1",
    )


def test_execute_fail_savefig_without_sender(mocker):
    # 目的: test_execute_fail_savefig_without_sender の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 0 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "システムエラーが発生しました。" である
    # reply_service: images, texts
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan)
    # Arrange
    mock = mocker.patch.object(
        reply_service,
        "push_a_message",
    )
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        "subplots",
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        "savefig",
        side_effect=FileNotFoundError(),
    )

    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    request_info_service.set_req_info(event=dummy_event)
    use_case = CreateMatchDetailGraphUseCase()

    # Act
    use_case.execute(1)

    # Assert
    assert len(reply_service.images) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "システムエラーが発生しました。"
    mock.assert_called_once_with(
        to=env_var.SERVER_ADMIN_LINE_USER_ID,
        message="対戦履歴の画像アップロードに失敗しました\n送信者: U0123456789abcdefghijklmnopqrstu1",
    )
