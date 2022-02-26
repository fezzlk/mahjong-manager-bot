from DomainService.GroupService import GroupService
from repositories import session_scope, group_repository
from tests.dummies import generate_dummy_group_list
from DomainModel.entities.Group import Group


def test_create_new_user():
    # Arrange
    group_service = GroupService()
    dummy_group = generate_dummy_group_list()[0]

    # Act
    result = group_service.find_or_create(dummy_group.line_group_id)

    # Assert
    assert isinstance(result, Group)
    assert result.line_group_id == dummy_group.line_group_id


def test_find_exist_group():
    # Arrange
    group_service = GroupService()
    dummy_group = generate_dummy_group_list()[0]
    with session_scope() as session:
        group_repository.create(session, dummy_group)

    # Act
    result = group_service.find_or_create(dummy_group.line_group_id)

    # Assert
    assert isinstance(result, Group)
    assert result.line_group_id == dummy_group.line_group_id
    with session_scope() as session:
        records = group_repository.find_all(session)
        assert len(records) == 1
