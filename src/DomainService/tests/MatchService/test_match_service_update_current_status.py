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


def test_success():
    # Arrange
    match_service = MatchService()
    target_match = dummy_matches[0]
    with session_scope() as session:
        for dummy_match in dummy_matches[0:3]:
            match_repository.create(session, dummy_match)

    # Act
    result: Match = match_service.update_current_status(
        line_group_id=target_match.line_group_id,
        status=0,
    )

    # Assert
    assert result.status == 0


def test_fail_not_found_match():
    with pytest.raises(ValueError):
        # Arrange
        match_service = MatchService()
        target_match = dummy_matches[3]
        with session_scope() as session:
            for dummy_match in dummy_matches[0:3]:
                match_repository.create(session, dummy_match)

        # Act
        result: Match = match_service.update_current_status(
            line_group_id=target_match.line_group_id,
            status=0,
        )

        # Assert
        assert result.status == 0
