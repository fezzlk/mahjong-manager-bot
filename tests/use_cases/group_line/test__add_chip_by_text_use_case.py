from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.match import Match
from domain_model.entities.user import User, UserMode
from repositories import (
    group_repository,
    match_repository,
    user_repository,
)
from use_cases.group_line.add_chip_by_text_use_case import AddChipByTextUseCase

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    _id=1,
)

dummy_users = [
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        mode=UserMode.wait.value,
        jantama_name="jantama_user1",
        _id=1,
    ),
    User(
        line_user_name="test_user2",
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        mode=UserMode.wait.value,
        jantama_name="jantama_user2",
        _id=2,
    ),
    User(
        line_user_name="test_user3",
        line_user_id="U0123456789abcdefghijklmnopqrstu3",
        mode=UserMode.wait.value,
        jantama_name="jantama_user3",
        _id=3,
    ),
    User(
        line_user_name="test_user4",
        line_user_id="U0123456789abcdefghijklmnopqrstu4",
        mode=UserMode.wait.value,
        jantama_name="jantama_user4",
        _id=4,
    ),
    User(
        line_user_name="test_user5",
        line_user_id="U0123456789abcdefghijklmnopqrstu5",
        mode=UserMode.wait.value,
        jantama_name="jantama_user5",
        _id=5,
    ),
]

dummy_matches = [
    Match(
        line_group_id=dummy_group.line_group_id,
        status=2,
        _id=1,
    ),
    Match(
        line_group_id=dummy_group.line_group_id,
        status=2,
        _id=2,
    ),
    Match(
        line_group_id=dummy_group.line_group_id,
        status=2,
        _id=3,
    ),
    Match(
        line_group_id=dummy_group.line_group_id,
        status=0,
        _id=4,
    ),
    Match(
        line_group_id="dummy",
        status=2,
        _id=5,
    ),
    Match(
        line_group_id="dummy",
        status=2,
        _id=6,
    ),
    Match(
        line_group_id="dummy",
        status=0,
        _id=7,
    ),
]


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / reply_service.texts[0].text が "test_user1: 10" である / len(matches[0].chip_scores) が len(expected_chip_scores) である / matches[0].chip_scores[k] が v である
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); user_repository.create(dummy_user); matches = match_repository.find(
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    dummy_group.active_match_id = 3
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text="10")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == "test_user1: 10"
    matches = match_repository.find(
        {
            "_id": 3,
        },
    )
    expected_chip_scores = {dummy_users[0].line_user_id: 10}
    assert len(matches[0].chip_scores) == len(expected_chip_scores)
    for k, v in expected_chip_scores.items():
        assert matches[0].chip_scores[k] == v


def test_execute_not_int_point():
    # 目的: test_execute_not_int_point の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / reply_service.texts[0].text が "整数で入力してください。" である / matches[0].chip_scores の件数が 0 件
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); user_repository.create(dummy_user); matches = match_repository.find()
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    dummy_group.active_match_id = 3
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text="hoge")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == "整数で入力してください。"
    matches = match_repository.find()
    assert len(matches[0].chip_scores) == 0


def test_execute_with_mention():
    # 目的: test_execute_with_mention の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / reply_service.texts[0].text が "test_user1: 10" である / len(matches[0].chip_scores) が len(expected_chip_scores) である / matches[0].chip_scores[k] が v である
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); user_repository.create(dummy_user); matches = match_repository.find(
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.mention_line_ids = ["U0123456789abcdefghijklmnopqrstu1"]
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    dummy_group.active_match_id = 3
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text="@test_user1 10")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == "test_user1: 10"
    matches = match_repository.find(
        {
            "_id": 3,
        },
    )
    expected_chip_scores = {"U0123456789abcdefghijklmnopqrstu1": 10}
    assert len(matches[0].chip_scores) == len(expected_chip_scores)
    for k, v in expected_chip_scores.items():
        assert matches[0].chip_scores[k] == v


def test_execute_multi_mentions():
    # 目的: test_execute_multi_mentions の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / ( / matches[0].chip_scores の件数が 0 件
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); user_repository.create(dummy_user); matches = match_repository.find(
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.mention_line_ids = [
        "U0123456789abcdefghijklmnopqrstu1",
        "U0123456789abcdefghijklmnopqrstu2",
    ]
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    dummy_group.active_match_id = 3
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text="@dummy1 @dummy2 10")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert (
        reply_service.texts[0].text
        == "メンションは1回につき1人を指定するようにしてください。"
    )
    matches = match_repository.find(
        {
            "_id": 3,
        },
    )
    assert len(matches[0].chip_scores) == 0


def test_execute_not_registered_user():
    # 目的: test_execute_not_registered_user の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / reply_service.texts[0].text が "友達未登録: 10" である / len(matches[0].chip_scores) が len(expected_chip_scores) である / matches[0].chip_scores[k] が v である
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); user_repository.create(dummy_user); matches = match_repository.find(
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.mention_line_ids = ["dummy_line_id"]
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    dummy_group.active_match_id = 3
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text="@dummy 10")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == "友達未登録: 10"
    matches = match_repository.find(
        {
            "_id": 3,
        },
    )
    expected_chip_scores = {"dummy_line_id": 10}
    assert len(matches[0].chip_scores) == len(expected_chip_scores)
    for k, v in expected_chip_scores.items():
        assert matches[0].chip_scores[k] == v


dummy_matches2 = [
    Match(
        line_group_id=dummy_group.line_group_id,
        status=2,
        _id=1,
        chip_scores={
            dummy_users[0].line_user_id: 20,
            dummy_users[1].line_user_id: -20,
        },
    ),
]


def test_execute_update():
    # 目的: test_execute_update の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / reply_service.texts[0].text が "test_user1: -10\ntest_user2: -20" である / len(matches[0].chip_scores) が len(expected_chip_scores) である / matches[0].chip_scores[k] が v である
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); user_repository.create(dummy_user); matches = match_repository.find(
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    for dummy_match in dummy_matches2:
        match_repository.create(dummy_match)
    dummy_group.active_match_id = 1
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text="-10")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == "test_user1: -10\ntest_user2: -20"
    matches = match_repository.find(
        {
            "_id": 1,
        },
    )
    expected_chip_scores = {
        dummy_users[0].line_user_id: -10,
        dummy_users[1].line_user_id: -20,
    }
    assert len(matches[0].chip_scores) == len(expected_chip_scores)
    for k, v in expected_chip_scores.items():
        assert matches[0].chip_scores[k] == v


def test_execute_delete():
    # 目的: test_execute_delete の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / reply_service.texts[0].text が "test_user2: -20" である / len(matches[0].chip_scores) が len(expected_chip_scores) である / matches[0].chip_scores[k] が v である
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); user_repository.create(dummy_user); matches = match_repository.find(
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    for dummy_match in dummy_matches2:
        match_repository.create(dummy_match)
    dummy_group.active_match_id = 1
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text="-")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == "test_user2: -20"
    matches = match_repository.find(
        {
            "_id": 1,
        },
    )
    expected_chip_scores = {
        dummy_users[1].line_user_id: -20,
    }
    assert len(matches[0].chip_scores) == len(expected_chip_scores)
    for k, v in expected_chip_scores.items():
        assert matches[0].chip_scores[k] == v


dummy_matches3 = [
    Match(
        line_group_id=dummy_group.line_group_id,
        status=2,
        _id=1,
        chip_scores={
            dummy_users[0].line_user_id: 20,
        },
    ),
]


def test_execute_delete_last_one():
    # 目的: test_execute_delete_last_one の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / reply_service.texts[0].text が "チップの増減枚数を入力して下さい。" である / len(matches[0].chip_scores) が len(expected_chip_scores) である / matches[0].chip_scores[k] が v である
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); user_repository.create(dummy_user); matches = match_repository.find(
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    for dummy_match in dummy_matches3:
        match_repository.create(dummy_match)
    dummy_group.active_match_id = 1
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text="-")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == "チップの増減枚数を入力して下さい。"
    matches = match_repository.find(
        {
            "_id": 1,
        },
    )
    expected_chip_scores = {}
    assert len(matches[0].chip_scores) == len(expected_chip_scores)
    for k, v in expected_chip_scores.items():
        assert matches[0].chip_scores[k] == v


def test_execute_no_active_match():
    # 目的: test_execute_no_active_match の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / reply_service.texts[0].text が "計算対象の試合が見つかりません。" である
    # reply_service: texts
    # DB操作: match_repository.create(dummy_match); group_repository.create(dummy_group); user_repository.create(dummy_user)
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    for dummy_match in dummy_matches3:
        match_repository.create(dummy_match)
    dummy_group.active_match_id = None
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text="-")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == "計算対象の試合が見つかりません。"


def test_execute_no_group():
    # 目的: test_execute_no_group の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].type が "text" である / (
    # reply_service: texts
    # DB操作: なし
    # Arrange
    use_case = AddChipByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id

    # Act
    use_case.execute(text="-")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert (
        reply_service.texts[0].text
        == "グループが登録されていません。招待し直してください。"
    )
