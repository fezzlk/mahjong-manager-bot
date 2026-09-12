from domain_model.entities.match import Match, MatchStatus
from domain_service import (
    match_service,
)
from repositories import match_repository

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"


def test_ok(mocker):
    # Arrange
    mock_count = mocker.patch.object(
        match_repository,
        "count",
        return_value=2,
    )

    # Act
    result = match_service.count_non_sim_by_line_group_id(_LINE_GROUP_ID)

    # Assert
    assert result == 2
    mock_count.assert_called_once_with({
        "line_group_id": _LINE_GROUP_ID,
        "status": {"$ne": MatchStatus.sim.value},
    })


def test_excludes_sim_sandbox():
    """statusがsimのMatchはカウント対象外(FEZ-66 Phase F)。"""
    match_repository.create(
        Match(line_group_id=_LINE_GROUP_ID, status=MatchStatus.open.value),
    )
    match_repository.create(
        Match(line_group_id=_LINE_GROUP_ID, status=MatchStatus.sim.value),
    )

    result = match_service.count_non_sim_by_line_group_id(_LINE_GROUP_ID)

    assert result == 1


def test_counts_open_and_settled_together():
    """open・settled問わず合算して数える(FEZ-66 Phase F)。"""
    match_repository.create(
        Match(line_group_id=_LINE_GROUP_ID, status=MatchStatus.open.value),
    )
    match_repository.create(
        Match(line_group_id=_LINE_GROUP_ID, status=MatchStatus.settled.value),
    )

    result = match_service.count_non_sim_by_line_group_id(_LINE_GROUP_ID)

    assert result == 2
