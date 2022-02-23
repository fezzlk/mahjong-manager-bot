import pytest
from DomainService.GroupService import GroupService
from repositories import session_scope, group_repository
from tests.dummies import generate_dummy_group_list


def test_success():
    # Arrange
    group_service = GroupService()
    dummy_groups = generate_dummy_group_list()[:3]
    dummy_group = dummy_groups[0]
    with session_scope() as session:
        for record in dummy_groups:
            group_repository.create(session, record)

    # Act
    result = group_service.get_zoom_url(
        line_group_id=dummy_group.line_group_id,
    )

    # Assert
    assert result == dummy_group.zoom_url


def test_not_hit():
    with pytest.raises(Exception):
        # Arrange
        group_service = GroupService()
        dummy_groups = generate_dummy_group_list()[:3]
        dummy_group = dummy_groups[0]
        with session_scope() as session:
            for record in dummy_groups[1:]:
                group_repository.create(session, record)

        # Act
        group_service.get_zoom_url(
            line_group_id=dummy_group.line_group_id,
        )

        # Assert
