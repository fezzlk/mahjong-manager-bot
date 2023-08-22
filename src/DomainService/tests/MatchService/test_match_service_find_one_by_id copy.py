from DomainService import (
    match_service,
)
from repositories import match_repository
from pymongo import ASCENDING


def test_ok(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        match_repository,
        'find',
    )

    # Act
    match_service.find_all_for_graph(ids=[1, 2], line_group_id='dummy')

    # Assert
    mock_find.assert_called_once_with(query={'_id': {'$in': [1,2]}}, sort=[('created_at', ASCENDING)])