from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match, MatchStatus
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
    current_input_match_id=1,
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
    # ノイズ用の無関係な他対戦(常にsettled固定): open対戦数のカウントに
    # 混入させないため(FEZ-66 Phase E、find_all_open_by_line_group_idで
    # 対戦を数えるようになった)。
    Match(
        line_group_id=dummy_group.line_group_id,
        status=MatchStatus.settled.value,
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
    # dummy_matchesが2件(このグループでは対戦名表示の閾値>1を超える)ため、
    # 対戦名「1」(name未設定なので_idにフォールバック)が先頭に付く(FEZ-66 Phase F)
    assert (
        reply_service.texts[0].text
        == "【対戦結果】 \n「1」\ntest_user1: 0pt (+100)\ntest_user2: 0pt (+20)\ntest_user3: 0pt (-40)\ntest_user4: 0pt (-40)\ntest_user5: 0pt (-40)"
    )
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.wait.value
    matches = match_repository.find({"_id": 1})
    assert not matches[0].is_deleted


def test_success():
    # 目的: test_success の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups[0].mode が GroupMode.wait.value である / groups[0].current_input_match_id is None / matches[0].status が 2 である / matches[0].chip_prices の件数が 5 件 / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu1"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu2"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu3"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu4"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu5"] が 0 である / matches[0].sum_scores の件数が 5 件 / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu1"] が 100 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu2"] が 20 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu3"] が -40 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu4"] が -40 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu5"] が -40 である / matches[0].sum_prices の件数が 5 件 / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu1"] が 5000 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu2"] が 1000 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu3"] が -2000 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu4"] が -2000 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu5"] が -2000 である / matches[0].sum_prices_with_chip の件数が 5 件 / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu1"] が 5000 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu2"] が 1000 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu3"] が -2000 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu4"] が -2000 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu5"] が -2000 である
    # reply_service: texts
    # DB操作: group_repository.create(; group_setting_repository.create(; user_repository.create(dummy_user); match_repository.create(dummy_match); hanchan_repository.create(dummy_hanchan); groups = group_repository.find({"line_group_id": dummy_group.line_group_id}); matches = match_repository.find({"_id": 1})
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.input.value,
            current_input_match_id=1,
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
    # dummy_matchesが2件(このグループでは対戦名表示の閾値>1を超える)ため、
    # 対戦名「1」(name未設定なので_idにフォールバック)が先頭に付く(FEZ-66 Phase F)
    assert (
        reply_service.texts[0].text
        == "【対戦結果】 \n「1」\ntest_user1: 5000pt (+100)\ntest_user2: 1000pt (+20)\n"
        + "test_user3: -2000pt (-40)\ntest_user4: -2000pt (-40)\ntest_user5: -2000pt (-40)"
    )
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.wait.value
    assert groups[0].current_input_match_id is None

    matches = match_repository.find({"_id": 1})
    assert not matches[0].is_deleted
    assert matches[0].status == MatchStatus.settled.value
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


def test_success_uses_match_settings_snapshot_over_group_settings():
    """精算はMatch自身が持つsettingsスナップショットを使い、グループの現在の
    設定は使わない(FEZ-66 Phase D)。異なるレートの対戦が同時に進行していても、
    それぞれ自分自身のレートで正しく精算されることを保証する。
    """
    # Arrange
    use_case = FinishMatchUseCase()
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    request_info_service.req_line_group_id = line_group_id
    group_repository.create(
        Group(
            line_group_id=line_group_id,
            mode=GroupMode.input.value,
            current_input_match_id=100,
            _id=100,
        ),
    )
    # グループの「現在の」設定はrate=5だが、対戦自身の設定はrate=9
    group_repository.update_settings(line_group_id, EmbeddedGroupSettings(rate=5))
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    match_repository.create(
        Match(
            line_group_id=line_group_id,
            settings=EmbeddedGroupSettings(rate=9),
            sum_scores={
                "U0123456789abcdefghijklmnopqrstu1": 100,
                "U0123456789abcdefghijklmnopqrstu2": 20,
                "U0123456789abcdefghijklmnopqrstu3": -40,
                "U0123456789abcdefghijklmnopqrstu4": -40,
                "U0123456789abcdefghijklmnopqrstu5": -40,
            },
            _id=100,
        ),
    )
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(
            Hanchan(
                line_group_id=line_group_id,
                raw_scores=dummy_hanchan.raw_scores,
                converted_scores=dummy_hanchan.converted_scores,
                match_id=100,
                is_deleted=dummy_hanchan.is_deleted,
            ),
        )

    # Act
    use_case.execute()

    # Assert: rate=9(対戦自身の設定)で精算されている(rate=5なら1000ptになるところ)
    assert len(reply_service.texts) == 1
    assert "test_user1: 9000pt (+100)" in reply_service.texts[0].text
    matches = match_repository.find({"_id": 100})
    assert matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu1"] == 9000


def test_success_with_chip_init():
    # 目的: test_success_with_chip_init の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups[0].mode が GroupMode.chip_input.value である / groups[0].current_input_match_id が 1 である
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
    assert groups[0].current_input_match_id == 1


def test_success_with_chip():
    # 目的: test_success_with_chip の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups[0].mode が GroupMode.wait.value である / groups[0].current_input_match_id is None / matches[0].status が 2 である / matches[0].chip_prices の件数が 5 件 / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu1"] が 150 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu2"] が -150 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu3"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu4"] が 0 である / matches[0].chip_prices["U0123456789abcdefghijklmnopqrstu5"] が 0 である / matches[0].sum_scores の件数が 5 件 / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu1"] が 100 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu2"] が 20 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu3"] が -40 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu4"] が -40 である / matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu5"] が -40 である / matches[0].sum_prices の件数が 5 件 / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu1"] が 0 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu2"] が 0 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu3"] が 0 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu4"] が 0 である / matches[0].sum_prices["U0123456789abcdefghijklmnopqrstu5"] が 0 である / matches[0].sum_prices_with_chip の件数が 5 件 / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu1"] が 150 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu2"] が -150 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu3"] が 0 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu4"] が 0 である / matches[0].sum_prices_with_chip["U0123456789abcdefghijklmnopqrstu5"] が 0 である
    # reply_service: texts
    # DB操作: group_repository.create(; group_setting_repository.create(dummy_group_setting); user_repository.create(dummy_user); match_repository.create(; hanchan_repository.create(dummy_hanchan); groups = group_repository.find({"line_group_id": dummy_group.line_group_id}); matches = match_repository.find()
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.chip_ok.value,
            current_input_match_id=1,
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
    assert groups[0].current_input_match_id is None
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
    """openな対戦が1件もなければ「見つかりません」を返す。

    「どの対戦が進行中か」の正本はMatch.statusであり(FEZ-66 Phase D/E)、
    group.current_input_match_idが何を指しているかとは無関係。
    """
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    # dummy_matches[1]はsettled固定のノイズ用データのみ作成し、openな対戦は
    # 1件も存在しない状態にする。
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


def test_execute_shows_picker_when_multiple_open_matches():
    """openな対戦が2件以上ならピッカーを表示し、どちらも精算しない
    (FEZ-66 Phase E)。
    """
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    group_repository.create(
        Group(line_group_id=line_group_id, mode=GroupMode.wait.value, _id=200),
    )
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    match_a = match_repository.create(
        Match(line_group_id=line_group_id, name="対戦A", status=MatchStatus.open.value),
    )
    match_b = match_repository.create(
        Match(line_group_id=line_group_id, name="対戦B", status=MatchStatus.open.value),
    )
    request_info_service.req_line_group_id = line_group_id

    FinishMatchUseCase().execute()

    assert len(reply_service.texts) == 1
    msg = reply_service.texts[0]
    assert msg.quick_reply is not None
    labels = {item.action.label for item in msg.quick_reply.items}
    assert labels == {"対戦A", "対戦B"}
    assert match_repository.find({"_id": match_a._id})[0].status == MatchStatus.open.value
    assert match_repository.find({"_id": match_b._id})[0].status == MatchStatus.open.value


def test_select_settles_only_the_chosen_match():
    """_finish_select?to=<id>で選択した対戦のみ精算し、他の進行中対戦には
    一切影響しない(FEZ-66 Phase E、複数系列同時進行の核心要件)。
    """
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    group_repository.create(
        Group(line_group_id=line_group_id, mode=GroupMode.wait.value, _id=201),
    )
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    target = match_repository.create(
        Match(
            line_group_id=line_group_id,
            name="精算対象",
            status=MatchStatus.open.value,
            sum_scores={"U0123456789abcdefghijklmnopqrstu1": 100},
        ),
    )
    other = match_repository.create(
        Match(
            line_group_id=line_group_id,
            name="他の対戦",
            status=MatchStatus.open.value,
            sum_scores={"U0123456789abcdefghijklmnopqrstu2": 999},
        ),
    )
    hanchan_repository.create(
        Hanchan(
            line_group_id=line_group_id,
            raw_scores={},
            converted_scores={"U0123456789abcdefghijklmnopqrstu1": 100},
            match_id=target._id,
        ),
    )
    request_info_service.req_line_group_id = line_group_id
    request_info_service.params = {"to": str(target._id)}

    FinishMatchUseCase().select()

    settled = match_repository.find({"_id": target._id})[0]
    untouched = match_repository.find({"_id": other._id})[0]
    assert settled.status == MatchStatus.settled.value
    assert untouched.status == MatchStatus.open.value
    assert untouched.sum_scores == {"U0123456789abcdefghijklmnopqrstu2": 999}


def test_select_invalid_match_id():
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    request_info_service.req_line_group_id = line_group_id
    request_info_service.params = {"to": "644c838186bbd9e20a91b785"}

    FinishMatchUseCase().select()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "指定された対戦が見つかりません。"


def test_select_malformed_match_id():
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    request_info_service.req_line_group_id = line_group_id
    request_info_service.params = {"to": "not-a-valid-object-id"}

    FinishMatchUseCase().select()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "指定された対戦が見つかりません。"


def test_select_blocked_while_another_match_is_mid_input():
    """他の対戦が入力セッション中(mode=input)なら、その対戦を選ばない限り
    精算をブロックする(FEZ-66 Phase E、他対戦のセッション破壊防止)。
    """
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    in_progress = match_repository.create(
        Match(line_group_id=line_group_id, name="入力中の対戦", status=MatchStatus.open.value),
    )
    group_repository.create(
        Group(
            line_group_id=line_group_id,
            mode=GroupMode.input.value,
            current_input_match_id=in_progress._id,
        ),
    )
    target = match_repository.create(
        Match(
            line_group_id=line_group_id,
            name="精算したい対戦",
            status=MatchStatus.open.value,
            sum_scores={"U0123456789abcdefghijklmnopqrstu1": 100},
        ),
    )
    hanchan_repository.create(
        Hanchan(
            line_group_id=line_group_id,
            raw_scores={},
            converted_scores={"U0123456789abcdefghijklmnopqrstu1": 100},
            match_id=target._id,
        ),
    )
    request_info_service.req_line_group_id = line_group_id
    request_info_service.params = {"to": str(target._id)}

    FinishMatchUseCase().select()

    assert len(reply_service.texts) == 1
    assert "入力中の対戦" in reply_service.texts[0].text
    assert match_repository.find({"_id": target._id})[0].status == MatchStatus.open.value


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
