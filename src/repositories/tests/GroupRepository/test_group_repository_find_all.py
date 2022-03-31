from tests.dummies import generate_dummy_group_list
from repositories import session_scope, group_repository
from DomainModel.entities.Group import Group


def test_success_find_records():
    # Arrange
    with session_scope() as session:
        dummy_groups = generate_dummy_group_list()[:3]
        for dummy_group in dummy_groups:
            group_repository.create(
                session,
                dummy_group,
            )

    # Act
    with session_scope() as session:
        result = group_repository.find_all(
            session,
        )

    # Assert
        assert len(result) == len(dummy_groups)
        for i in range(len(result)):
            assert isinstance(result[i], Group)
            assert result[i]._id == dummy_groups[i]._id
            assert result[i].line_group_id == dummy_groups[i].line_group_id
            assert result[i].zoom_url == dummy_groups[i].zoom_url
            assert result[i].mode == dummy_groups[i].mode


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    with session_scope() as session:
        result = group_repository.find_all(
            session,
        )

    # Assert
        assert len(result) == 0
