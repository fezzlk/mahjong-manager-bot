from typing import List, Tuple
import pytest
from DomainModel.entities.Match import Match
from DomainService.MatchService import MatchService
from repositories import session_scope, match_repository

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[0, 1],
        users=[],
        status=1,
        _id=0,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[2, 3],
        users=[],
        status=0,
        _id=1,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[4, 5],
        users=[],
        status=2,
        _id=2,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        hanchan_ids=[4, 5],
        users=[],
        status=0,
        _id=3,
    ),
]


@pytest.fixture(params=[
    # (added_hanchan_id, updated_hanchan_ids)
    (2, [0, 1, 2]),
    (1, [0, 1]),
])
def case(request) -> Tuple[int, List[int]]:
    return request.param


def test_success(case):
    # Arrange
    match_service = MatchService()
    target_match = dummy_matches[0]
    with session_scope() as session:
        for dummy_match in dummy_matches[0:3]:
            match_repository.create(session, dummy_match)

    # Act
    result: Match = match_service.add_hanchan_id(
        line_group_id=target_match.line_group_id,
        hanchan_id=case[0],
    )

    # Assert
    expected = case[1]
    assert len(result.hanchan_ids) == len(expected)
    for i in range(len(expected)):
        assert result.hanchan_ids[i] == expected[i]


def test_fail_not_found_match():
    with pytest.raises(ValueError):
        # Arrange
        match_service = MatchService()
        target_match = dummy_matches[3]
        with session_scope() as session:
            for dummy_match in dummy_matches[0:3]:
                match_repository.create(session, dummy_match)

        # Act
        match_service.add_hanchan_id(
            line_group_id=target_match.line_group_id,
            hanchan_id=2,
        )

        # Assert


def test_success_with_valid_line_group_id_and_not_active():
    with pytest.raises(ValueError):
        # Arrange
        match_service = MatchService()
        target_match = dummy_matches[1]
        with session_scope() as session:
            for dummy_match in dummy_matches[1:4]:
                match_repository.create(session, dummy_match)

        # Act
        match_service.add_hanchan_id(
            line_group_id=target_match.line_group_id,
            hanchan_id=2,
        )

        # Assert
