from pymongo import DESCENDING

from domain_model.entities.match import Match, MatchStatus
from domain_service import (
    match_service,
)
from repositories import match_repository

dummy_matches = [
    Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    ),
    Match(
        _id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    ),
]

_EXPECTED_QUERY = {
    "line_group_id": "G0123456789abcdefghijklmnopqrstu1",
    "status": {"$ne": MatchStatus.sim.value},
}


def test_ok(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        match_repository,
        "find",
        return_value=dummy_matches,
    )

    # Act
    result = match_service.find_latest_one("G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert isinstance(result, Match)
    mock_find.assert_called_once_with(query=_EXPECTED_QUERY, sort=[("created_at", DESCENDING)])


def test_ok_no_hit(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        match_repository,
        "find",
        return_value=[],
    )

    # Act
    result = match_service.find_latest_one("G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert result is None
    mock_find.assert_called_once_with(query=_EXPECTED_QUERY, sort=[("created_at", DESCENDING)])


def test_excludes_sim_sandbox_even_if_more_recent():
    """statusがsimのMatchは、他より新しくても最新対戦として返らない(FEZ-66 Phase C)。"""
    match_repository.create(
        Match(line_group_id="G0123456789abcdefghijklmnopqrstu1", status=MatchStatus.settled.value),
    )
    match_repository.create(
        Match(line_group_id="G0123456789abcdefghijklmnopqrstu1", status=MatchStatus.sim.value),
    )

    result = match_service.find_latest_one("G0123456789abcdefghijklmnopqrstu1")

    assert result.status == MatchStatus.settled.value
