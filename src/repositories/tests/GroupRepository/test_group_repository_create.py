from tests.dummies import generate_dummy_group_list
from repositories import session_scope, group_repository


def test_success():
    # Arrange
    dummy_group = generate_dummy_group_list()[0]

    # Act
    with session_scope() as session:
        group_repository.create(
            session,
            dummy_group,
        )

    # Assert
    with session_scope() as session:
        result = group_repository.find_all(
            session,
        )
        assert len(result) == 1
        assert result[0].line_group_id == dummy_group.line_group_id
        assert result[0].zoom_url == dummy_group.zoom_url
        assert result[0].mode == dummy_group.mode
