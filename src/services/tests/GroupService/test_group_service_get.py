from services.GroupService import GroupService
from repositories import session_scope, group_repository
from tests.dummies import generate_dummy_group_list
from domains.Group import Group


def test_find_all():
    # Arrange
    group_service = GroupService()
    dummy_groups = generate_dummy_group_list()[:3]
    with session_scope() as session:
        for dummy_group in dummy_groups:
            group_repository.create(session, dummy_group)

    # Act
    result = group_service.get()

    # Assert
    assert len(result) == len(dummy_groups)
    for i in range(len(result)):
        assert isinstance(result[i], Group)
        assert result[i]._id == dummy_groups[i]._id
        assert result[i].line_group_id == dummy_groups[i].line_group_id
        assert result[i].mode == dummy_groups[i].mode
        assert result[i].zoom_url == dummy_groups[i].zoom_url


def test_find_some_groups():
    # Arrange
    group_service = GroupService()
    dummy_groups = generate_dummy_group_list()[:3]
    with session_scope() as session:
        for dummy_group in dummy_groups:
            group_repository.create(session, dummy_group)
    target_group_id_list = [
        dummy_groups[0]._id,
        dummy_groups[1]._id,
    ]

    # Act
    result = group_service.get(
        ids=target_group_id_list,
    )

    # Assert
    assert len(result) == len(target_group_id_list)
    for i in range(len(result)):
        assert isinstance(result[i], Group)
        assert result[i]._id == dummy_groups[i]._id
        assert result[i].line_group_id == dummy_groups[i].line_group_id
        assert result[i].mode == dummy_groups[i].mode
        assert result[i].zoom_url == dummy_groups[i].zoom_url
