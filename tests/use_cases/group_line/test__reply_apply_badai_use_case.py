from datetime import datetime

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.match import Match
from domain_model.entities.user import User
from line_models.event import Event
from repositories import (
    match_repository,
    user_repository,
)
from use_cases.group_line.reply_apply_badai_use_case import ReplyApplyBadaiUseCase

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
            "U0123456789abcdefghijklmnopqrstu1": 30,
            "U0123456789abcdefghijklmnopqrstu2": 60,
            "U0123456789abcdefghijklmnopqrstu3": -60,
            "U0123456789abcdefghijklmnopqrstu4": -10,
            "U0123456789abcdefghijklmnopqrstu5": -10,
            "dummy": -10,
        },
        sum_prices={
            "U0123456789abcdefghijklmnopqrstu1": 900,
            "U0123456789abcdefghijklmnopqrstu2": 1800,
            "U0123456789abcdefghijklmnopqrstu3": -1800,
            "U0123456789abcdefghijklmnopqrstu4": -300,
            "U0123456789abcdefghijklmnopqrstu5": -300,
            "dummy": -300,
        },
        chip_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu4": -10,
        },
        chip_prices={
            "U0123456789abcdefghijklmnopqrstu1": 100,
            "U0123456789abcdefghijklmnopqrstu4": -100,
        },
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
        is_deleted=True,
        created_at=datetime(2010, 1, 1, 1, 1, 3),
    ),
    Match(
        _id=4,
        line_group_id="dummy",
        created_at=datetime(2010, 1, 1, 1, 1, 4),
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
    text="_badai 3,000",
)


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / reply_service.texts[0].text が "直前の対戦の最終会計を表示します。" である / (
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); user_repository.create(dummy_user)
    # Arrange
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute("3,000")

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == "直前の対戦の最終会計を表示します。"
    assert (
        reply_service.texts[1].text
        == "対戦開始日: 2010年01月01日\n場代: 3000pt(500pt×6人)\ntest_user1: 500pt\ntest_user2: 1300pt\ntest_user3: -2300pt\ntest_user4: -900pt\ntest_user5: -800pt\n友達未登録: -800pt"
    )


def test_execute_with_fraction():
    # 目的: test_execute_with_fraction の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / reply_service.texts[0].text が "直前の対戦の最終会計を表示します。" である / (
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); user_repository.create(dummy_user)
    # Arrange
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute("2,996")

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == "直前の対戦の最終会計を表示します。"
    assert (
        reply_service.texts[1].text
        == "対戦開始日: 2010年01月01日\n場代: 2996pt(500pt×6人-4pt)\ntest_user1: 500pt\ntest_user2: 1300pt\ntest_user3: -2300pt\ntest_user4: -900pt\ntest_user5: -800pt\n友達未登録: -800pt"
    )


def test_execute_invalid_badai():
    # 目的: test_execute_invalid_badai の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "場代は自然数で入力してください。" である
    # reply_service: texts
    # DB操作: なし
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute("dummy")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "場代は自然数で入力してください。"


def test_execute_no_match():
    # 目的: test_execute_no_match の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "まだ対戦結果がありません。" である
    # reply_service: texts
    # DB操作: なし
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute("0")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "まだ対戦結果がありません。"


def test_execute_with_progress_match():
    # 目的: test_execute_with_progress_match の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / (
    # reply_service: texts
    # DB操作: match_repository.create(progress_match); user_repository.create(dummy_user)
    # Arrange
    progress_match = Match(
        _id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        created_at=datetime(2010, 1, 1, 1, 1, 2),
        sum_scores={
            "U0123456789abcdefghijklmnopqrstu1": 30,
            "U0123456789abcdefghijklmnopqrstu2": 60,
            "U0123456789abcdefghijklmnopqrstu3": -60,
            "U0123456789abcdefghijklmnopqrstu4": -10,
            "U0123456789abcdefghijklmnopqrstu5": -10,
            "dummy": -10,
        },
        sum_prices={
            "U0123456789abcdefghijklmnopqrstu1": 900,
            "U0123456789abcdefghijklmnopqrstu2": 1800,
            "U0123456789abcdefghijklmnopqrstu3": -1800,
            "U0123456789abcdefghijklmnopqrstu4": -300,
            "U0123456789abcdefghijklmnopqrstu5": -300,
            "dummy": -300,
        },
        chip_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10,
            "U0123456789abcdefghijklmnopqrstu4": -10,
        },
        chip_prices={
            "U0123456789abcdefghijklmnopqrstu1": 100,
            "U0123456789abcdefghijklmnopqrstu4": -100,
        },
        sum_prices_with_chip={},
    )
    match_repository.create(progress_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute("2,996")

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "現在進行中の対戦があります。対戦を終了するには「_finish」と送信してください。"
    )


def test_execute_with_progress_match2():
    # 目的: test_execute_with_progress_match2 の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / (
    # reply_service: texts
    # DB操作: match_repository.create(progress_match); user_repository.create(dummy_user)
    # Arrange
    progress_match = Match(
        _id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        created_at=datetime(2010, 1, 1, 1, 1, 2),
    )
    match_repository.create(progress_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyApplyBadaiUseCase()

    # Act
    use_case.execute("2,996")

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "現在進行中の対戦があります。対戦を終了するには「_finish」と送信してください。"
    )
