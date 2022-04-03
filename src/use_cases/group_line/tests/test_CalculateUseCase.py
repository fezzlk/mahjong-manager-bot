import pytest
from DomainModel.entities.UserMatch import UserMatch
from use_cases.group_line.CalculateUseCase import CalculateUseCase
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from DomainModel.entities.Config import Config
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Group import Group, GroupMode

from repositories import (
    session_scope,
    user_repository,
    hanchan_repository,
    match_repository,
    group_repository,
    user_match_repository,
)

from ApplicationService import (
    reply_service,
    request_info_service,
)

dummy_users = [
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        zoom_url="https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user1",
        matches=[],
        _id=1,
    ),
    User(
        line_user_name="test_user2",
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        zoom_url="https://us00web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user2",
        matches=[],
        _id=2,
    ),
    User(
        line_user_name="test_user3",
        line_user_id="U0123456789abcdefghijklmnopqrstu3",
        zoom_url="https://us00web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user3",
        matches=[],
        _id=3,
    ),
    User(
        line_user_name="test_user4",
        line_user_id="U0123456789abcdefghijklmnopqrstu4",
        zoom_url="https://us00web.zoom.us/j/01234567894?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user4",
        matches=[],
        _id=4,
    ),
    User(
        line_user_name="test_user5",
        line_user_id="U0123456789abcdefghijklmnopqrstu5",
        zoom_url="https://us00web.zoom.us/j/01234567895?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user5",
        matches=[],
        _id=5,
    ),
]

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    zoom_url="https://us01web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
    mode=GroupMode.wait,
    _id=1,
)

dummy_match = Match(
    line_group_id=dummy_group.line_group_id,
    hanchan_ids=[],
    users=[],
    status=1,
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
    converted_scores={},
    match_id=1,
    status=2,
    _id=1,
)

dummy_current_hanchan = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 40000,
        dummy_users[1].line_user_id: 30000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[3].line_user_id: 10000,
    },
    converted_scores={},
    match_id=1,
    status=1,
    _id=2,
)

dummy_current_hanchan_with_other_user = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 40000,
        dummy_users[1].line_user_id: 30000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[4].line_user_id: 10000,
    },
    converted_scores={},
    match_id=1,
    status=1,
    _id=2,
)

dummy_configs = [
    Config(
        target_id=dummy_users[0].line_user_id,
        key='飛び賞',
        value='30',
        _id=1,
    ),
    Config(
        target_id=dummy_users[0].line_user_id,
        key='飛び賞',
        value='30',
        _id=1,
    ),
    Config(
        target_id=dummy_users[0].line_user_id,
        key='飛び賞',
        value='30',
        _id=1,
    ),
]


@ pytest.fixture(params=[
    # index of (
    # dummy_points_list,
    # dummy_converted_scores_list)
    (0),
])
def case1(request) -> int:
    return request.param


def test_success():
    # Arrange
    use_case = CalculateUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    with session_scope() as session:
        group_repository.create(session, dummy_group)
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_current_hanchan)

    # Act
    use_case.execute()

    # Assert
    expected_c_scores = {
        dummy_users[0].line_user_id: 50,
        dummy_users[1].line_user_id: 10,
        dummy_users[2].line_user_id: -20,
        dummy_users[3].line_user_id: -40,
    }
    with session_scope() as session:
        hanchan = hanchan_repository.find_all(session)[0]
        for k in expected_c_scores:
            assert hanchan.converted_scores[k] == expected_c_scores[k]
        assert hanchan.status == 2
        um = user_match_repository.find_by_user_ids(
            session,
            [1, 2, 3, 4]
        )
        assert len(um) == 4
        assert len(reply_service.texts) == 4
        assert reply_service.texts[1].text == "test_user1: +50 (+50)\ntest_user2: +10 (+10)\ntest_user3: -20 (-20)\ntest_user4: -40 (-40)"
        group = group_repository.find_one_by_line_group_id(
            session, dummy_group.line_group_id)
        assert group.mode == GroupMode.wait

        reply_service.reset()


def test_success_update_user_matches():
    # Arrange
    use_case = CalculateUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    with session_scope() as session:
        group_repository.create(session, dummy_group)
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_archived_hanchan)
        hanchan_repository.create(
            session, dummy_current_hanchan_with_other_user)
        for user_id in [1, 2, 3, 4]:
            um = UserMatch(user_id, dummy_match._id)
            user_match_repository.create(session, um)

    # Act
    use_case.execute()

    # Assert
    with session_scope() as session:
        um = user_match_repository.find_by_user_ids(
            session,
            [1, 2, 3, 4, 5]
        )
        assert len(um) == 5

        reply_service.reset()


# def test_success_not_active_hanchan():
#     # Arrange
#     use_case = CalculateUseCase()
#     dummy_tobashita_player_id = 'a'

#     # Act
#     result = use_case.execute(tobashita_player_id=dummy_tobashita_player_id)

#     # Assert
#     expected = dummy_converted_scores_list1[case1[1]]
#     assert len(result) == len(expected)
#     for key in result:
#         assert result[key] == expected[key]


# def test_success_does_not_have_4_points():
#     # Arrange
#     use_case = CalculateUseCase()
#     dummy_tobashita_player_id = 'a'

#     # Act
#     result = use_case.execute(tobashita_player_id=dummy_tobashita_player_id)

#     # Assert
#     expected = dummy_converted_scores_list1[case1[1]]
#     assert len(result) == len(expected)
#     for key in result:
#         assert result[key] == expected[key]


# def test_success_does_invalid_sum_point():
#     # Arrange
#     use_case = CalculateUseCase()
#     dummy_tobashita_player_id = 'a'

#     # Act
#     result = use_case.execute(tobashita_player_id=dummy_tobashita_player_id)

#     # Assert
#     expected = dummy_converted_scores_list1[case1[1]]
#     assert len(result) == len(expected)
#     for key in result:
#         assert result[key] == expected[key]


# def test_success_with_tobi():
#     # Arrange
#     use_case = CalculateUseCase()
#     dummy_tobashita_player_id = 'a'

#     # Act
#     result = use_case.execute(tobashita_player_id=dummy_tobashita_player_id)

#     # Assert
#     expected = dummy_converted_scores_list1[case1[1]]
#     assert len(result) == len(expected)
#     for key in result:
#         assert result[key] == expected[key]


# def test_success_reply_tobi_menu():
#     # Arrange
#     use_case = CalculateUseCase()
#     with session_scope() as session:
#         group_repository.create(session, dummy_group)
#         for dummy_user in dummy_users:
#             user_repository.create(session, dummy_user)
#         match_repository.create(session, dummy_match)
#         hanchan_repository.create(session, dummy_hanchans[0])

#     # Act
#     result = use_case.execute()

#     # Assert
#     expected = dummy_converted_scores_list1[case1[1]]
#     assert len(result) == len(expected)
#     for key in result:
#         assert result[key] == expected[key]


# def test_success_other_configs():
#     # Arrange
#     use_case = CalculateUseCase()
#     with session_scope() as session:
#         group_repository.create(session, dummy_group)
#         for dummy_user in dummy_users:
#             user_repository.create(session, dummy_user)
#         match_repository.create(session, dummy_match)
#         hanchan_repository.create(session, dummy_hanchans[0])

#     # Act
#     result = use_case.execute()

#     # Assert
#     expected = dummy_converted_scores_list1[case1[1]]
#     assert len(result) == len(expected)
#     for key in result:
#         assert result[key] == expected[key]
