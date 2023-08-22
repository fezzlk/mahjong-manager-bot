from DomainService import (
    user_match_service,
)
from repositories import user_match_repository



def test_ok(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_match_repository,
        'find',
    )

    # Act
    user_match_service.find_all_by_user_id_list(user_ids=[1, 2])

    # Assert
    mock_find.assert_called_once_with({'user_id': {'$in': [1,2]}})