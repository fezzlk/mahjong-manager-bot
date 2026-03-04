from datetime import datetime
from typing import Dict

import matplotlib.pyplot as plt
import pytest

import env_var
from application_service import (
    graph_service,
    reply_service,
    request_info_service,
)
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from domain_model.entities.user import User
from domain_model.entities.user_match import UserMatch
from line_models.event import Event
from repositories import (
    hanchan_repository,
    match_repository,
    user_match_repository,
    user_repository,
)
from use_cases.group_line.reply_multi_history_use_case import ReplyMultiHistoryUseCase

dummy_matches = [
    Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        created_at=datetime(2010, 1, 1, 1, 1, 1),
    ),
    Match(
        _id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        sum_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu4": -10,
        },
    ),
    Match(
        _id=3,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        is_deleted=True,
        created_at=datetime(2010, 1, 1, 1, 1, 3),
    ),
    Match(
        _id=4,
        line_group_id="dummy",
        created_at=datetime(2010, 1, 1, 1, 1, 4),
    ),
    Match(
        _id=5,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        created_at=datetime(2010, 1, 1, 1, 1, 1),
        sum_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu4": -10,
        },
    ),
]

dummy_hanchans = [
    Hanchan(
        _id=1,
        match_id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        is_deleted=True,
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

dummy_user_matches = [
    UserMatch(
        user_id=1,
        match_id=1,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=1,
    ),
    UserMatch(
        user_id=2,
        match_id=1,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=2,
    ),
    UserMatch(
        user_id=3,
        match_id=1,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=3,
    ),
    UserMatch(
        user_id=4,
        match_id=1,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=4,
    ),
    UserMatch(
        user_id=1,
        match_id=2,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=5,
    ),
    UserMatch(
        user_id=2,
        match_id=2,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=6,
    ),
    UserMatch(
        user_id=3,
        match_id=2,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=7,
    ),
    UserMatch(
        user_id=4,
        match_id=2,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=8,
    ),
    UserMatch(
        user_id=5,
        match_id=2,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=9,
    ),
    UserMatch(
        user_id=1,
        match_id=5,
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        _id=10,
    ),
]

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="_history",
)


@pytest.fixture(params=[
    "?from=x",
    "?to=x",
    "?from=20230101&to=x",
    "?from=x&to=20230101",
    "?from=x&to=x",
])
def case1(request) -> Dict[str, str]:
    return request.param


def test_execute_with_invalid_range_format(case1):
    # 目的: test_execute_with_invalid_range_format の挙動を検証する。
    # 入力: case1
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 0 件 / reply_service.texts の件数が 2 件 / reply_service.texts[0].text が "日付は以下のフォーマットで入力してください。" である / reply_service.texts[1].text が "[日付の入力方法]\n\nYYYY年MM月DD日\n→ YYYYMMDD\n\n20YY年MM月DD日\n→ YYMMDD\n\n今年MM月DD日\n→ MMDD\n\n今月DD日\n→ DD" である
    # reply_service: images, texts
    # DB操作: user_repository.create(dummy_user); user_match_repository.create(dummy_user_match)
    # Arrange
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_user_match in dummy_user_matches:
        user_match_repository.create(dummy_user_match)
    dummy_event1 = Event(
        type="message",
        source_type="group",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        group_id="G0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text="_history" + case1,
    )
    request_info_service.set_req_info(event=dummy_event1)
    use_case = ReplyMultiHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.images) == 0
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == "日付は以下のフォーマットで入力してください。"
    assert reply_service.texts[1].text == "[日付の入力方法]\n\nYYYY年MM月DD日\n→ YYYYMMDD\n\n20YY年MM月DD日\n→ YYMMDD\n\n今年MM月DD日\n→ MMDD\n\n今月DD日\n→ DD"


def test_execute(mocker):
    # 目的: test_execute の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 1 件
    # reply_service: images
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_repository.create(dummy_user); user_match_repository.create(dummy_user_match)
    # Arrange
    fig, _ = plt.subplots()
    mocker.patch.object(graph_service, "build_history_step_graph", return_value=fig)
    mocker.patch.object(fig, "savefig")
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_user_match in dummy_user_matches:
        user_match_repository.create(dummy_user_match)

    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyMultiHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.images) == 1


@pytest.fixture(params=[
    ("?from=20230101", "範囲指定: 2023年01月01日0時から"),
    ("?to=20241231", "範囲指定: 2024年12月31日0時まで"),
    ("?from=20230101&to=20241231", "範囲指定: 2023年01月01日0時から2024年12月31日0時まで"),
])
def case2(request) -> Dict[str, str]:
    return request.param


def test_execute_with_range(mocker, case2):
    # 目的: test_execute_with_range の挙動を検証する。
    # 入力: mocker, case2
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 1 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が case2[1] である
    # reply_service: images, texts
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_repository.create(dummy_user); user_match_repository.create(dummy_user_match)
    # Arrange
    fig, _ = plt.subplots()
    mocker.patch.object(graph_service, "build_history_step_graph", return_value=fig)
    mocker.patch.object(fig, "savefig")

    dummy_user_matches_local = [
        UserMatch(
            user_id=1,
            match_id=1,
            created_at=datetime(2010, 1, 1, 1, 1, 2),
            _id=1,
        ),
        UserMatch(
            user_id=1,
            match_id=2,
            created_at=datetime(2010, 1, 1, 1, 1, 2),
            _id=5,
        ),
        UserMatch(
            user_id=1,
            match_id=5,
            created_at=datetime(2023, 1, 1, 1, 1, 2),
            _id=10,
        ),
    ]

    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_user_match in dummy_user_matches_local:
        user_match_repository.create(dummy_user_match)
    dummy_event2 = Event(
        type="message",
        source_type="group",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        group_id="G0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text="_history" + case2[0],
    )
    request_info_service.set_req_info(event=dummy_event2)
    use_case = ReplyMultiHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.images) == 1
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == case2[1]


def test_execute_fail_savefig(mocker):
    # 目的: test_execute_fail_savefig の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 0 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "システムエラーが発生しました。" である
    # reply_service: images, texts
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_repository.create(dummy_user); user_match_repository.create(dummy_user_match)
    # Arrange
    mock = mocker.patch.object(
        reply_service,
        "push_a_message",
    )
    fig, _ = plt.subplots()
    mocker.patch.object(graph_service, "build_history_step_graph", return_value=fig)
    mocker.patch.object(fig, "savefig", side_effect=FileNotFoundError())

    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_user_match in dummy_user_matches:
        user_match_repository.create(dummy_user_match)

    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyMultiHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.images) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "システムエラーが発生しました。"
    mock.assert_called_once_with(
        to=env_var.SERVER_ADMIN_LINE_USER_ID,
        message="対戦履歴の画像アップロードに失敗しました\n送信者: test_user1",
    )


def test_execute_no_match(mocker):
    # 目的: test_execute_no_match の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "対局履歴がありません。" である
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_repository.create(dummy_user)
    # Arrange
    fig, _ = plt.subplots()
    mocker.patch.object(graph_service, "build_history_step_graph", return_value=fig)
    mocker.patch.object(fig, "savefig")

    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyMultiHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "対局履歴がありません。"


def test_execute_contain_unknown_user(mocker):
    # 目的: test_execute_contain_unknown_user の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 1 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "友達登録されていないユーザは表示されません。" である
    # reply_service: images, texts
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_repository.create(dummy_user); user_match_repository.create(dummy_user_match)
    # Arrange
    fig, _ = plt.subplots()
    mocker.patch.object(graph_service, "build_history_step_graph", return_value=fig)
    mocker.patch.object(fig, "savefig")

    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_user_match in dummy_user_matches:
        user_match_repository.create(dummy_user_match)

    request_info_service.set_req_info(event=Event(
        type="message",
        source_type="group",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        group_id="G0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text="_graph",
        mention_ids=[
            "U0123456789abcdefghijklmnopqrstu2",
            "dummy",
        ],
    ))
    use_case = ReplyMultiHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.images) == 1
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "友達登録されていないユーザは表示されません。"


def test_execute_with_mention(mocker):
    # 目的: test_execute_with_mention の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 1 件
    # reply_service: images
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_repository.create(dummy_user); user_match_repository.create(dummy_user_match)
    # Arrange
    fig, _ = plt.subplots()
    mocker.patch.object(graph_service, "build_history_step_graph", return_value=fig)
    mocker.patch.object(fig, "savefig")

    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_user_match in dummy_user_matches:
        user_match_repository.create(dummy_user_match)

    request_info_service.set_req_info(event=Event(
        type="message",
        source_type="group",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        group_id="G0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text="_graph",
        mention_ids=[
            "U0123456789abcdefghijklmnopqrstu2",
            "U0123456789abcdefghijklmnopqrstu3",
        ],
    ))
    use_case = ReplyMultiHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.images) == 1
