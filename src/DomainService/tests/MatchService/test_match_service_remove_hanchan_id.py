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
        _id=1,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[2, 3],
        users=[],
        status=0,
        _id=2,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[4, 5],
        users=[],
        status=2,
        _id=3,
    ),
]


@pytest.fixture(params=[
    # (match_id, removed_hanchan_id, updated_hanchan_ids)
    (1, 1, [0]),
    (1, 2, [0, 1]),
    (2, 3, [2]),  # disabled match
    (3, 5, [4]),  # archived match
])
def case(request) -> Tuple[int, int, List[int]]:
    return request.param


def test_success(case):
    # Arrange
    match_service = MatchService()
    with session_scope() as session:
        for dummy_match in dummy_matches[0:3]:
            match_repository.create(session, dummy_match)

    # Act
    result: Match = match_service.remove_hanchan_id(
        match_id=case[0],
        hanchan_id=case[1],
    )

    # Assert
    expected = case[2]
    assert len(result.hanchan_ids) == len(expected)
    for i in range(len(expected)):
        assert result.hanchan_ids[i] == expected[i]


def test_fail_not_found_match():
    with pytest.raises(ValueError):
        # Arrange
        match_service = MatchService()
        with session_scope() as session:
            for dummy_match in dummy_matches[0:2]:
                match_repository.create(session, dummy_match)

        # Act
        match_service.remove_hanchan_id(
            match_id=3,
            hanchan_id=1,
        )

        # Assert
