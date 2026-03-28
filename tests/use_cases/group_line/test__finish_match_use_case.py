from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from domain_model.entities.user import User, UserMode
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_repository,
)
from use_cases.group_line.finish_match_use_case import FinishMatchUseCase

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

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    active_match_id=1,
    _id=1,
)

dummy_matches = [
    Match(
        line_group_id=dummy_group.line_group_id,
        sum_scores={
            "U0123456789abcdefghijklmnopqrstu1": 100,
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu3": -40,
            "U0123456789abcdefghijklmnopqrstu4": -40,
            "U0123456789abcdefghijklmnopqrstu5": -40,
        },
        _id=1,
    ),
    Match(
        line_group_id=dummy_group.line_group_id,
        _id=2,
    ),
]

dummy_hanchans = [
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[0].line_user_id: 40000,
            dummy_users[1].line_user_id: 30000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 10000,
        },
        converted_scores={
            dummy_users[0].line_user_id: 50,
            dummy_users[1].line_user_id: 10,
            dummy_users[2].line_user_id: -20,
            dummy_users[3].line_user_id: -40,
        },
        match_id=1,
        _id=1,
    ),
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[0].line_user_id: 40000,
            dummy_users[1].line_user_id: 30000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[4].line_user_id: 10000,
        },
        converted_scores={
            dummy_users[0].line_user_id: 50,
            dummy_users[1].line_user_id: 10,
            dummy_users[2].line_user_id: -20,
            dummy_users[4].line_user_id: -40,
        },
        match_id=1,
        _id=2,
    ),
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[0].line_user_id: 40000,
            dummy_users[1].line_user_id: 30000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 10000,
        },
        converted_scores={
            dummy_users[0].line_user_id: 50,
            dummy_users[1].line_user_id: 10,
            dummy_users[2].line_user_id: -20,
            dummy_users[3].line_user_id: -40,
        },
        match_id=1,
        is_deleted=True,
        _id=3,
    ),
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[0].line_user_id: 40000,
            dummy_users[1].line_user_id: 30000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 10000,
        },
        converted_scores={
            dummy_users[0].line_user_id: 50,
            dummy_users[1].line_user_id: 10,
            dummy_users[2].line_user_id: -20,
            dummy_users[3].line_user_id: -40,
        },
        match_id=2,
        _id=4,
    ),
]


def test_success_with_default_settings():
    # 目的: test_success_with_default_settings の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups[0].mode が GroupMode.wait.value である / matches[0].status が 2 である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); user_repository.create(dummy_user); match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); groups = group_repository.find({"line_group_id": dummy_group.line_group_id}); matches = match_repository.find({"_id": 1})
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "【対戦結果】 \ntest_user1: 0pt (+100)\ntest_user2: 0pt (+20)\ntest_user3: 0pt (-40)\ntest_user4: 0pt (-40)\ntest_user5: 0pt (-40)"
    )
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.wait.value
    matches = match_repository.find({"_id": 1})
    assert not matches[0].is_deleted


def test_success():
    # 目的: test_success の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups[0].mode が GroupMode.wait.value である / groups[0].active_match_id is None / matches[0].status が 2 である / matches[0].chip_prices の件数が 5 件 / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu1"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu2"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu3"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu4"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu5"] が 0 である / matches[0].sum_scores の件数が 5 件 / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu1"] が 100 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu2"] が 20 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu3"] が -40 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu4"] が -40 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu5"] が -40 である / matches[0].sum_prices の件数が 5 件 / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu1"] が 5000 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu2"] が 1000 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu3"] が -2000 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu4"] が -2000 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu5"] が -2000 である / matches[0].sum_prices_with_chip の件数が 5 件 / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu1"] が 5000 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu2"] が 1000 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu3"] が -2000 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu4"] が -2000 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu5"] が -2000 である
    # reply_service: texts
    # DB操作: group_repository.create(; group_setting_repository.create(; user_repository.create(dummy_user); match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); groups = group_repository.find({"line_group_id": dummy_group.line_group_id}); matches = match_repository.find({"_id": 1})
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.input.value,
            active_match_id=1,
            _id=1,
        ),
    )
    group_repository.update_settings(
        "G0123456789abcdefghijklmnopqrstu1",
        EmbeddedGroupSettings(rate=5),
    )
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "【対戦結果】 \ntest_user1: 5000pt (+100)\ntest_user2: 1000pt (+20)\n"
        + "test_user3: -2000pt (-40)\ntest_user4: -2000pt (-40)\ntest_user5: -2000pt (-40)"
    )
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.wait.value
    assert groups[0].active_match_id is None

    matches = match_repository.find({"_id": 1})
    assert not matches[0].is_deleted
    assert matches[0].chip_prices == {}
    assert len(matches[0].sum_scores) == 5
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu1"] == 100
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu2"] == 20
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu3"] == -40
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu4"] == -40
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu5"] == -40
    assert len(matches[0].sum_prices) == 5
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu1"] == 5000
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu2"] == 1000
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu3"] == -2000
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu4"] == -2000
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu5"] == -2000
    assert len(matches[0].sum_prices_with_chip) == 5
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu1"] == 5000
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu2"] == 1000
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu3"] == -2000
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu4"] == -2000
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu5"] == -2000


def test_success_with_chip_init():
    # 目的: test_success_with_chip_init の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups[0].mode が GroupMode.chip_input.value である / groups[0].active_match_id が 1 である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); group_setting_repository.create(; user_repository.create(dummy_user); match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    group_repository.update_settings(
        "G0123456789abcdefghijklmnopqrstu1",
        EmbeddedGroupSettings(chip_rate=1),
    )
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 0
    assert len(reply_service.buttons) == 1
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.chip_input.value
    assert groups[0].active_match_id == 1


def test_success_with_chip():
    # 目的: test_success_with_chip の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups[0].mode が GroupMode.wait.value である / groups[0].active_match_id is None / matches[0].status が 2 である / matches[0].chip_prices の件数が 5 件 / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu1"] が 150 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu2"] が -150 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu3"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu4"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu5"] が 0 である / matches[0].sum_scores の件数が 5 件 / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu1"] が 100 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu2"] が 20 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu3"] が -40 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu4"] が -40 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu5"] が -40 である / matches[0].sum_prices の件数が 5 件 / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu1"] が 0 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu2"] が 0 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu3"] が 0 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu4"] が 0 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu5"] が 0 である / matches[0].sum_prices_with_chip の件数が 5 件 / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu1"] が 150 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu2"] が -150 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu3"] が 0 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu4"] が 0 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu5"] が 0 である
    # reply_service: texts
    # DB操作: group_repository.create(; group_setting_repository.create(dummy_group_setting); user_repository.create(dummy_user); match_repository.create(; hanchan_repository.create(dummy_hanchan); groups = group_repository.find({"line_group_id": dummy_group.line_group_id}); matches = match_repository.find()
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.chip_ok.value,
            active_match_id=1,
            _id=1,
        ),
    )
    group_repository.update_settings(
        "G0123456789abcdefghijklmnopqrstu1",
        EmbeddedGroupSettings(rate=5, chip_rate=1),
    )
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    match_repository.create(
        Match(
            line_group_id=dummy_group.line_group_id,
            chip_scores={
                "U0123456789abcdefghijklmnopqrstu1": 3,
                "U0123456789abcdefghijklmnopqrstu2": -3,
            },
            sum_scores={
                "U0123456789abcdefghijklmnopqrstu1": 100,
                "U0123456789abcdefghijklmnopqrstu2": 20,
                "U0123456789abcdefghijklmnopqrstu3": -40,
                "U0123456789abcdefghijklmnopqrstu4": -40,
                "U0123456789abcdefghijklmnopqrstu5": -40,
            },
            _id=1,
        ),
    )
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "【対戦結果】 \ntest_user1: 5150pt (+100 / チップ+3枚)\ntest_user2: 850pt (+20 / チップ-3枚)\n"
        + "test_user3: -2000pt (-40 / チップ0枚)\ntest_user4: -2000pt (-40 / チップ0枚)\ntest_user5: -2000pt (-40 / チップ0枚)"
    )
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.wait.value
    assert groups[0].active_match_id is None
    matches = match_repository.find()
    assert not matches[0].is_deleted
    assert matches[0].chip_prices == {}
    assert len(matches[0].sum_scores) == 5
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu1"] == 100
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu2"] == 20
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu3"] == -40
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu4"] == -40
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu5"] == -40
    assert len(matches[0].sum_prices) == 5
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu1"] == 5000
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu2"] == 1000
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu3"] == -2000
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu4"] == -2000
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu5"] == -2000
    assert len(matches[0].sum_prices_with_chip) == 5
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu1"] == 5150
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu2"] == 850
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu3"] == -2000
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu4"] == -2000
    assert matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu5"] == -2000


def test_success_without_active_match():
    # 目的: test_success_without_active_match の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "計算対象の試合が見つかりません。" である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); user_repository.create(dummy_user); match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan)
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_match in dummy_matches[1:]:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "計算対象の試合が見つかりません。"


def test_success_without_hanchan():
    # 目的: test_success_without_hanchan の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "まだ対戦結果がありません。" である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); user_repository.create(dummy_user); match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan)
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans[2:]:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "まだ対戦結果がありません。"


def test_ng_no_group():
    # 目的: test_ng_no_group の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / (
    # reply_service: texts
    # DB操作: user_repository.create(dummy_user); match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan)
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans[2:]:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "グループが登録されていません。招待し直してください。"
    )
