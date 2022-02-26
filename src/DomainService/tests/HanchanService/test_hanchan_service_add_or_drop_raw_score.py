import pytest
from DomainModel.entities.Match import Match
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.User import User, UserMode
from DomainService.HanchanService import HanchanService
from repositories import session_scope, hanchan_repository, match_repository

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[],
        users=[],
        status=1,
        _id=1,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        hanchan_ids=[],
        users=[],
        status=1,
        _id=2,
    ),
]

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
]

dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={
            dummy_users[0].line_user_id: 10000,
            dummy_users[1].line_user_id: 20000,
        },
        converted_scores={},
        match_id=1,
        status=1,
        _id=1,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={
            dummy_users[0].line_user_id: 10000,
            dummy_users[1].line_user_id: 20000,
        },
        converted_scores={},
        match_id=1,
        status=2,
        _id=2,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={},
        converted_scores={},
        match_id=1,
        status=0,
        _id=3,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        raw_scores={},
        converted_scores={},
        match_id=2,
        status=0,
        _id=4,
    ),
]


def test_success_add_point():
    # Arrange
    hanchan_service = HanchanService()
    target_hanchan = dummy_hanchans[0]
    with session_scope() as session:
        for dummy_match in dummy_matches[0:2]:
            match_repository.create(session, dummy_match)

        for dummy_hanchan in dummy_hanchans[0:3]:
            hanchan_repository.create(session, dummy_hanchan)

    # Act
    result: Hanchan = hanchan_service.add_or_drop_raw_score(
        line_group_id=target_hanchan.line_group_id,
        line_user_id=dummy_users[2].line_user_id,
        raw_score=40000
    )

    # Assert
    expected = {
        dummy_users[0].line_user_id: 10000,
        dummy_users[1].line_user_id: 20000,
        dummy_users[2].line_user_id: 40000,
    }
    assert result._id == target_hanchan._id
    assert result.line_group_id == target_hanchan.line_group_id
    assert len(result.raw_scores) == len(target_hanchan.raw_scores) + 1
    for luid in result.raw_scores:
        assert result.raw_scores[luid] == expected[luid]


def test_success_update_point():
    # Arrange
    hanchan_service = HanchanService()
    target_hanchan = dummy_hanchans[0]
    with session_scope() as session:
        for dummy_match in dummy_matches[0:2]:
            match_repository.create(session, dummy_match)

        for dummy_hanchan in dummy_hanchans[0:3]:
            hanchan_repository.create(session, dummy_hanchan)

    # Act
    result: Hanchan = hanchan_service.add_or_drop_raw_score(
        line_group_id=target_hanchan.line_group_id,
        line_user_id=dummy_users[1].line_user_id,
        raw_score=30000,
    )

    # Assert
    expected = {
        dummy_users[0].line_user_id: 10000,
        dummy_users[1].line_user_id: 30000,
    }
    assert result._id == target_hanchan._id
    assert result.line_group_id == target_hanchan.line_group_id
    assert len(result.raw_scores) == len(expected)
    for luid in result.raw_scores:
        assert result.raw_scores[luid] == expected[luid]


def test_success_drop_point():
    # Arrange
    hanchan_service = HanchanService()
    target_hanchan = dummy_hanchans[0]
    with session_scope() as session:
        for dummy_match in dummy_matches[0:2]:
            match_repository.create(session, dummy_match)

        for dummy_hanchan in dummy_hanchans[0:3]:
            hanchan_repository.create(session, dummy_hanchan)

    # Act
    result: Hanchan = hanchan_service.add_or_drop_raw_score(
        line_group_id=target_hanchan.line_group_id,
        line_user_id=dummy_users[1].line_user_id,
        raw_score=None,
    )

    # Assert
    expected = {
        dummy_users[0].line_user_id: 10000,
    }
    assert result._id == target_hanchan._id
    assert result.line_group_id == target_hanchan.line_group_id
    assert len(result.raw_scores) == len(expected)
    for luid in result.raw_scores:
        assert result.raw_scores[luid] == expected[luid]


@pytest.fixture(params=[
    # (index_of_dummy_hanchans)
    (0),  # not active
    (3),  # not exist
])
def case(request) -> int:
    return request.param


def test_fail_not_found_hanchan(case):
    with pytest.raises(ValueError):
        # Arrange
        hanchan_service = HanchanService()
        target_hanchan = dummy_hanchans[case]
        with session_scope() as session:
            for dummy_match in dummy_matches[0:2]:
                match_repository.create(session, dummy_match)

            for dummy_hanchan in dummy_hanchans[1:2]:
                hanchan_repository.create(session, dummy_hanchan)

        # Act
        hanchan_service.add_or_drop_raw_score(
            line_group_id=target_hanchan.line_group_id,
            line_user_id=dummy_users[1].line_user_id,
            raw_score=None,
        )

        # Assert


def test_fail_no_arg_line_user_id():
    with pytest.raises(ValueError):
        # Arrange
        hanchan_service = HanchanService()
        target_hanchan = dummy_hanchans[0]
        with session_scope() as session:
            for dummy_match in dummy_matches[0:2]:
                match_repository.create(session, dummy_match)

            for dummy_hanchan in dummy_hanchans[0:3]:
                hanchan_repository.create(session, dummy_hanchan)

        # Act
        hanchan_service.add_or_drop_raw_score(
            line_group_id=target_hanchan.line_group_id,
            line_user_id=None,
            raw_score=30000,
        )
        # Assert
