from DomainModel.entities.Match import Match
from DomainService.MatchService import MatchService
from repositories import session_scope, match_repository
from tests.dummies import generate_dummy_match_list

dummy_matches = generate_dummy_match_list()[0:5]


def test_success():
    # Arrange
    match_service = MatchService()
    target_match = dummy_matches[0]
    with session_scope() as session:
        for dummy_match in dummy_matches[0:3]:
            match_repository.create(session, new_match=dummy_match)

    # Act
    result = match_service.get_or_create_current(
        line_group_id=target_match.line_group_id
    )

    # Assert
    assert isinstance(result, Match)
    assert result._id == target_match._id
    assert result.line_group_id == target_match.line_group_id
    assert result.status == target_match.status
    assert result.hanchan_ids == target_match.hanchan_ids


def test_success_with_valid_line_group_id_and_not_active():
    # Arrange
    match_service = MatchService()
    target_match = dummy_matches[0]
    with session_scope() as session:
        for dummy_match in dummy_matches[1:3]:
            match_repository.create(session, new_match=dummy_match)

    # Act
    result = match_service.get_or_create_current(
        line_group_id=target_match.line_group_id
    )

    # Assert
    assert isinstance(result, Match)
    assert result.line_group_id == target_match.line_group_id
    assert result.status == 1
    assert result.hanchan_ids == []


def test_success_not_found_line_group_id():
    # Arrange
    match_service = MatchService()
    target_match = dummy_matches[4]
    with session_scope() as session:
        for dummy_match in dummy_matches[0:4]:
            match_repository.create(session, new_match=dummy_match)

    # Act
    result = match_service.get_or_create_current(
        line_group_id=target_match.line_group_id
    )

    # Assert
    assert isinstance(result, Match)
    assert result.line_group_id == target_match.line_group_id
    assert result.status == 1
    assert result.hanchan_ids == []
