from datetime import datetime

from DomainModel.entities.UserMatch import UserMatch
from DomainService import (
    user_match_service,
)
from repositories import user_match_repository

dummy_user_match = UserMatch(
    user_id=1,
    match_id=2,
)


def test_ok(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_match_repository,
        "find",
        return_value=[dummy_user_match],
    )

    # Act
    result = user_match_service.find_all_by_user_id_list(user_ids=[1, 2])

    # Assert
    assert len(result) == 1
    assert result[0].user_id == dummy_user_match.user_id
    assert result[0].match_id == dummy_user_match.match_id
    mock_find.assert_called_once_with(query={"$and": [{"user_id": {"$in": [1, 2]}}]})


def test_ok_with_from_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_match_repository,
        "find",
        return_value=[dummy_user_match],
    )

    # Act
    result = user_match_service.find_all_by_user_id_list(user_ids=[1, 2], from_dt=datetime(2022, 1, 2, 3, 4, 5))

    # Assert
    assert len(result) == 1
    assert result[0].user_id == dummy_user_match.user_id
    assert result[0].match_id == dummy_user_match.match_id
    mock_find.assert_called_once_with(query={"$and": [{"user_id": {"$in": [1, 2]}}, {"created_at": {"$gte": datetime(2022, 1, 2, 3, 4, 5)}}]})


def test_ok_with_to_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_match_repository,
        "find",
        return_value=[dummy_user_match],
    )

    # Act
    result = user_match_service.find_all_by_user_id_list(user_ids=[1, 2], to_dt=datetime(2022, 1, 2, 3, 4, 5))

    # Assert
    assert len(result) == 1
    assert result[0].user_id == dummy_user_match.user_id
    assert result[0].match_id == dummy_user_match.match_id
    mock_find.assert_called_once_with(query={"$and": [{"user_id": {"$in": [1, 2]}}, {"created_at": {"$lte": datetime(2022, 1, 2, 3, 4, 5)}}]})


def test_ok_with_both_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_match_repository,
        "find",
        return_value=[dummy_user_match],
    )

    # Act
    result = user_match_service.find_all_by_user_id_list(user_ids=[1, 2], from_dt=datetime(2022, 1, 2, 3, 4, 5), to_dt=datetime(2023, 1, 2, 3, 4, 5))

    # Assert
    assert len(result) == 1
    assert result[0].user_id == dummy_user_match.user_id
    assert result[0].match_id == dummy_user_match.match_id
    mock_find.assert_called_once_with(query={"$and": [{"user_id": {"$in": [1, 2]}}, {"created_at": {"$gte": datetime(2022, 1, 2, 3, 4, 5)}}, {"created_at": {"$lte": datetime(2023, 1, 2, 3, 4, 5)}}]})
