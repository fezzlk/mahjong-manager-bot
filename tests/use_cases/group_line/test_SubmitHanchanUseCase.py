from copy import deepcopy

from pymongo import ASCENDING

from ApplicationService import (
    calculate_service,
    reply_service,
    request_info_service,
)
from DomainModel.entities.Group import Group, GroupMode
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.UserHanchan import UserHanchan
from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_hanchan_repository,
    user_match_repository,
    user_repository,
)
from use_cases.group_line.SubmitHanchanUseCase import SubmitHanchanUseCase

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

dummy_match = Match(
    line_group_id=dummy_group.line_group_id,
    status=2,
    _id=1,
)

dummy_archived_hanchan = Hanchan(
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
)

dummy_disabled_hanchan = Hanchan(
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
)

dummy_active_hanchan = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 40010,
        dummy_users[1].line_user_id: 30000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[3].line_user_id: 10000,
    },
    converted_scores={},
    match_id=1,
    status=2,
    _id=1,
)

dummy_active_hanchan_with_other_user = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 40000,
        dummy_users[1].line_user_id: 30000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[4].line_user_id: 10000,
    },
    converted_scores={},
    match_id=1,
    status=2,
)

dummy_active_hanchan_has_5_points = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 40000,
        dummy_users[1].line_user_id: 30000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[3].line_user_id: 10000,
        dummy_users[4].line_user_id: 0,
    },
    converted_scores={},
    match_id=1,
    status=2,
)

dummy_active_hanchan_has_invalid_sum_point = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 50000,
        dummy_users[1].line_user_id: 30000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[3].line_user_id: 10000,
    },
    converted_scores={},
    match_id=1,
    status=2,
)

dummy_active_hanchan_has_tai = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 35000,
        dummy_users[1].line_user_id: 35000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[3].line_user_id: 10000,
    },
    converted_scores={},
    match_id=1,
    status=2,
)

dummy_active_hanchan_has_minus_point = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 60000,
        dummy_users[1].line_user_id: 30000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[3].line_user_id: -10000,
    },
    converted_scores={},
    match_id=1,
    status=2,
)


def test_success():
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_active_hanchan)
    dummy_match.active_hanchan_id = dummy_active_hanchan._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    expected_c_scores = {
        dummy_users[0].line_user_id: 50,
        dummy_users[1].line_user_id: 10,
        dummy_users[2].line_user_id: -20,
        dummy_users[3].line_user_id: -40,
    }
    hanchan = hanchan_repository.find()[0]
    for k, v in expected_c_scores.items():
        assert hanchan.converted_scores[k] == v
    assert hanchan.status == 2
    um = user_match_repository.find(
        {"user_id": {"$in": [1, 2, 3, 4]}},
    )
    assert len(um) == 4
    assert len(reply_service.texts) == 3
    assert len(reply_service.buttons) == 1
    assert (
        reply_service.texts[1].text
        == "test_user1: +50 (+50)\ntest_user2: +10 (+10)\ntest_user3: -20 (-20)\ntest_user4: -40 (-40)"
    )
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.wait.value
    matches = match_repository.find({"_id": 1})
    assert matches[0].active_hanchan_id is None
    assert len(matches[0].sum_scores) == 4
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu1"] == 50
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu2"] == 10
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu3"] == -20
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu4"] == -40

    expected_uhs = [
        UserHanchan(
            line_user_id="U0123456789abcdefghijklmnopqrstu1",
            hanchan_id=1,
            point=40010,
            rank=1,
            yakuman_count=0,
        ),
        UserHanchan(
            line_user_id="U0123456789abcdefghijklmnopqrstu2",
            hanchan_id=1,
            point=30000,
            rank=2,
            yakuman_count=0,
        ),
        UserHanchan(
            line_user_id="U0123456789abcdefghijklmnopqrstu3",
            hanchan_id=1,
            point=20000,
            rank=3,
            yakuman_count=0,
        ),
        UserHanchan(
            line_user_id="U0123456789abcdefghijklmnopqrstu4",
            hanchan_id=1,
            point=10000,
            rank=4,
            yakuman_count=0,
        ),
    ]
    uhs = user_hanchan_repository.find(sort=[("rank", ASCENDING)])
    for i in range(len(uhs)):
        assert uhs[i].line_user_id == expected_uhs[i].line_user_id
        assert uhs[i].hanchan_id == expected_uhs[i].hanchan_id
        assert uhs[i].point == expected_uhs[i].point
        assert uhs[i].rank == expected_uhs[i].rank
        assert uhs[i].yakuman_count == expected_uhs[i].yakuman_count

    reply_service.reset()


def test_success_assert_sum_point_in_match():
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    dm = deepcopy(dummy_match)
    hanchan_repository.create(dummy_archived_hanchan)
    hanchan_repository.create(dummy_disabled_hanchan)
    hanchan_repository.create(dummy_active_hanchan_with_other_user)
    dm.active_hanchan_id = dummy_active_hanchan_with_other_user._id
    match_repository.create(dm)

    # Act
    use_case.execute()

    # Assert
    hanchan_repository.find()
    assert (
        reply_service.texts[1].text
        == "test_user1: +50 (+100)\ntest_user2: +10 (+20)\ntest_user3: -20 (-40)\ntest_user5: -40 (-40)"
    )
    matches = match_repository.find({"_id": 1})
    assert matches[0].active_hanchan_id is None
    assert len(matches[0].sum_scores) == 5
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu1"] == 100
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu2"] == 20
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu3"] == -40
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu4"] == -40
    assert matches[0].sum_scores["U0123456789abcdefghijklmnopqrstu5"] == -40

    reply_service.reset()


def test_success_update_user_matches():
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_archived_hanchan)
    hanchan_repository.create(dummy_active_hanchan_with_other_user)
    dummy_match.active_hanchan_id = dummy_active_hanchan_with_other_user._id
    match_repository.create(dummy_match)
    for user_id in [1, 2, 3, 4]:
        um = UserMatch(user_id, dummy_match._id)
        user_match_repository.create(um)

    # Act
    use_case.execute()

    # Assert
    um = user_match_repository.find(
        {"user_id": {"$in": [1, 2, 3, 4, 5]}},
    )
    assert len(um) == 5

    reply_service.reset()


def test_success_not_active_hanchan(mocker):
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_archived_hanchan)
    hanchan_repository.create(dummy_disabled_hanchan)
    match_repository.create(dummy_match)

    mock = mocker.patch.object(
        calculate_service,
        "run",
        return_value=None,
    )

    # Act
    use_case.execute()

    # Assert
    assert mock.call_count == 0
    um = user_match_repository.find(
        {"user_id": {"$in": [1, 2, 3, 4]}},
    )
    assert len(um) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "計算対象の半荘が見つかりません。"
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.input.value

    reply_service.reset()


def test_success_does_not_have_4_points():
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_active_hanchan_has_5_points)
    dummy_match.active_hanchan_id = dummy_active_hanchan_has_5_points._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    hanchan = hanchan_repository.find()[0]
    assert len(hanchan.converted_scores) == 0
    um = user_match_repository.find(
        {"user_id": {"$in": [1, 2, 3, 4]}},
    )
    assert len(um) == 0
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "四人分の点数を入力してください。点数を取り消したい場合は @[ユーザー名] と送ってください。"
    )
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.input.value
    matches = match_repository.find({"_id": 1})
    assert matches[0].active_hanchan_id == dummy_active_hanchan_has_5_points._id

    reply_service.reset()


def test_success_does_invalid_sum_point():
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_active_hanchan_has_invalid_sum_point)
    dummy_match.active_hanchan_id = dummy_active_hanchan_has_invalid_sum_point._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    hanchan = hanchan_repository.find()[0]
    assert len(hanchan.converted_scores) == 0
    um = user_match_repository.find(
        {"user_id": {"$in": [1, 2, 3, 4]}},
    )
    assert len(um) == 0
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "点数の合計が110000点です。合計100000点+αになるように修正してください。"
    )
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.input.value
    matches = match_repository.find({"_id": 1})
    assert (
        matches[0].active_hanchan_id == dummy_active_hanchan_has_invalid_sum_point._id
    )

    reply_service.reset()


def test_success_has_tai():
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_active_hanchan_has_tai)
    dummy_match.active_hanchan_id = dummy_active_hanchan_has_tai._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    hanchan = hanchan_repository.find()[0]
    assert len(hanchan.converted_scores) == 0
    um = user_match_repository.find(
        {"user_id": {"$in": [1, 2, 3, 4]}},
    )
    assert len(um) == 0
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "同点のユーザーがいます。上家が1点でも高くなるよう修正してください。"
    )
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.input.value
    matches = match_repository.find({"_id": 1})
    assert matches[0].active_hanchan_id == dummy_active_hanchan_has_tai._id

    reply_service.reset()


def test_success_reply_tobi_menu():
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_active_hanchan_has_minus_point)
    dummy_match.active_hanchan_id = dummy_active_hanchan_has_minus_point._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.buttons) == 1
    hanchan = hanchan_repository.find()[0]
    assert len(hanchan.converted_scores) == 0
    um = user_match_repository.find(
        {"user_id": {"$in": [1, 2, 3, 4]}},
    )
    assert len(um) == 0
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.input.value
    matches = match_repository.find({"_id": 1})
    assert matches[0].active_hanchan_id == dummy_active_hanchan_has_minus_point._id

    reply_service.reset()


def test_fail_no_active_match():
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    dummy_group.active_match_id = None
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_active_hanchan)
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    hanchan = hanchan_repository.find()[0]
    assert len(hanchan.converted_scores) == 0
    um = user_match_repository.find(
        {"user_id": {"$in": [1, 2, 3, 4]}},
    )
    assert len(um) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "計算対象の試合が見つかりません。"
    groups = group_repository.find({"line_group_id": dummy_group.line_group_id})
    assert groups[0].mode == GroupMode.input.value

    reply_service.reset()


def test_fail_no_group():
    # Arrange
    use_case = SubmitHanchanUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_active_hanchan)
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    hanchan = hanchan_repository.find()[0]
    assert len(hanchan.converted_scores) == 0
    um = user_match_repository.find(
        {"user_id": {"$in": [1, 2, 3, 4]}},
    )
    assert len(um) == 0
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "グループが登録されていません。招待し直してください。"
    )

    reply_service.reset()
