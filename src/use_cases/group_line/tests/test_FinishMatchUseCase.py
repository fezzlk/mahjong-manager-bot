from DomainModel.entities.GroupSetting import GroupSetting
from use_cases.group_line.FinishMatchUseCase import FinishMatchUseCase
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Group import Group, GroupMode
from repositories import (
    user_repository,
    hanchan_repository,
    match_repository,
    group_repository,
    group_setting_repository,
)

from ApplicationService import (
    reply_service,
    request_info_service,
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

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    _id=1,
)

dummy_matches = [
    Match(
        line_group_id=dummy_group.line_group_id,
        status=1,
        _id=1,
    ),
    Match(
        line_group_id=dummy_group.line_group_id,
        status=2,
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
        status=2,
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
        status=2,
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
        status=0,
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
        status=2,
    ),
]


def test_success_with_default_settings():
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
    assert reply_service.texts[0].text == \
        "対戦ID: 1\ntest_user1: 0円 (+100(0枚))\ntest_user2: 0円 (+20(0枚))\ntest_user3: 0円 (-40(0枚))\ntest_user4: 0円 (-40(0枚))\ntest_user5: 0円 (-40(0枚))"
    groups = group_repository.find({'line_group_id': dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.wait.value
    matches = match_repository.find({'_id': 1})
    assert matches[0].status == 2


def test_success():
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        mode=GroupMode.input.value,
        _id=1,
    ))
    group_setting_repository.create(GroupSetting(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        rate=5,
    ))
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
    assert reply_service.texts[0].text == "対戦ID: 1\ntest_user1: 5000円 (+100(0枚))\ntest_user2: 1000円 (+20(0枚))\n" + \
        "test_user3: -2000円 (-40(0枚))\ntest_user4: -2000円 (-40(0枚))\ntest_user5: -2000円 (-40(0枚))"
    groups = group_repository.find({'line_group_id': dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.wait.value
    matches = match_repository.find({'_id': 1})
    assert matches[0].status == 2


def test_success_with_tip_init():
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    group_setting_repository.create(GroupSetting(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        tip_rate=50,
    ))
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
    assert reply_service.texts[0].text == 'チップの増減数を入力してください。完了したら「_tip_ok」と入力してください。'
    groups = group_repository.find({'line_group_id': dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.tip_input.value
    matches = match_repository.find({'_id': 1})
    assert matches[0].status == 1


def test_success_with_tip():
    # Arrange
    use_case = FinishMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        mode=GroupMode.tip_ok.value,
        _id=1,
    ))
    dummy_group_setting = GroupSetting(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        tip_rate=50,
    )
    group_setting_repository.create(dummy_group_setting)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    match_repository.create(Match(
        line_group_id=dummy_group.line_group_id,
        tip_scores={"U0123456789abcdefghijklmnopqrstu1": 3, "U0123456789abcdefghijklmnopqrstu2": -3},
        status=1,
        _id=1,
    ))
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "対戦ID: 1\ntest_user1: 150円 (+100(+3枚))\ntest_user2: -150円 (+20(-3枚))\n" + \
        "test_user3: 0円 (-40(0枚))\ntest_user4: 0円 (-40(0枚))\ntest_user5: 0円 (-40(0枚))"
    groups = group_repository.find({'line_group_id': dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.wait.value
    matches = match_repository.find({'_id': 1})
    assert matches[0].status == 2


def test_success_without_current_match():
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
    assert reply_service.texts[0].text == 'まだ対戦結果がありません。'


def test_success_without_hanchan():
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
    assert reply_service.texts[0].text == 'まだ対戦結果がありません。'
