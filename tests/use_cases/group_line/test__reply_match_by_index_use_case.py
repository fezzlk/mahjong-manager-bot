from datetime import datetime

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
from use_cases.group_line.reply_match_by_index_use_case import ReplyMatchByIndexUseCase

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
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 30,
            "U0123456789abcdefghijklmnopqrstu2": 60,
            "U0123456789abcdefghijklmnopqrstu3": -30,
            "U0123456789abcdefghijklmnopqrstu4": -60,
        },
        match_id=2,
        status=2,
        _id=1,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu3": -30,
            "U0123456789abcdefghijklmnopqrstu4": 50,
            "U0123456789abcdefghijklmnopqrstu5": -10,
            "dummy": -10,
        },
        match_id=2,
        status=2,
        _id=2,
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
    text="_match 2",
)


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / ( / ( / reply_service.images の件数が 1 件
    # reply_service: images, texts
    # DB操作: match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); user_repository.create(dummy_user)
    # Arrange
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyMatchByIndexUseCase()

    # Act
    use_case.execute("2")

    # Assert
    assert len(reply_service.texts) == 2
    assert (
        reply_service.texts[0].text
        == "第2回\n2010年01月01日\ntest_user1: 1000円 (+30(+10枚))\ntest_user2: 1800円 (+60(0枚))\ntest_user3: -1800円 (-60(0枚))\ntest_user4: -400円 (-10(-10枚))\ntest_user5: -300円 (-10(0枚))\n友達未登録: -300円 (-10(0枚))"
    )
    assert (
        reply_service.texts[1].text
        == "【半荘情報】\n\n第1回\ntest_user2: +60 (+60)\ntest_user1: +30 (+30)\ntest_user3: -30 (-30)\ntest_user4: -60 (-60)\n\n第2回\ntest_user4: +50 (-10)\ntest_user5: -10 (-10)\n友達未登録: -10 (-10)\ntest_user3: -30 (-60)"
    )
    assert len(reply_service.images) == 1


def test_execute_invalid_arg():
    # 目的: test_execute_invalid_arg の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "引数は整数で指定してください。" である / reply_service.images の件数が 0 件
    # reply_service: images, texts
    # DB操作: match_repository.create(dummy_match); user_repository.create(dummy_user)
    # Arrange
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyMatchByIndexUseCase()

    # Act
    use_case.execute("dummy")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "引数は整数で指定してください。"
    assert len(reply_service.images) == 0


def test_execute_out_of_index():
    # 目的: test_execute_out_of_index の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / reply_service.images の件数が 0 件
    # reply_service: images, texts
    # DB操作: match_repository.create(dummy_match); user_repository.create(dummy_user)
    # Arrange
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyMatchByIndexUseCase()

    # Act
    use_case.execute("3")

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "このトークルームには全2回までしか登録されていないため第3回はありません。"
    )
    assert len(reply_service.images) == 0
