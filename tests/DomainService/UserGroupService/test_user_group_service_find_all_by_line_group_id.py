from DomainModel.entities.UserGroup import UserGroup
from DomainService import (
    user_group_service,
)
from repositories import user_group_repository

dummy_user_group = UserGroup(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
    )


def test_ok_hit_match(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_group_repository,
        "find",
        return_value=[dummy_user_group],
    )

    # Act
    result = user_group_service.find_all_by_line_group_id("G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert len(result) == 1
    assert result[0]._id == dummy_user_group._id
    assert result[0].line_group_id == dummy_user_group.line_group_id
    assert result[0].line_user_id == dummy_user_group.line_user_id
    mock_find.assert_called_once_with(query={"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})
