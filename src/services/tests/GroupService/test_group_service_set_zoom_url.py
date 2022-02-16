import pytest
from Services.GroupService import GroupService
from Repositories import session_scope, group_repository
from tests.dummies import generate_dummy_group_list


def test_success():
    # Arrange
    group_service = GroupService()
    dummy_groups = generate_dummy_group_list()[:3]
    dummy_group = dummy_groups[0]
    with session_scope() as session:
        for record in dummy_groups:
            group_repository.create(session, record)
    assert_zoom_url = [
        "https://us01web.zoom.us/j/0123456789x?pwd=abcdefghijklmnopqrstuvwxyz",
        "https://us01web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
        "https://us01web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
    ]

    # Act
    result = group_service.set_zoom_url(
        line_group_id=dummy_group.line_group_id,
        zoom_url="https://us01web.zoom.us/j/0123456789x?pwd=abcdefghijklmnopqrstuvwxyz",
    )

    # Assert
    assert result.zoom_url == assert_zoom_url[0]
    with session_scope() as session:
        records_on_db = group_repository.find_all(session)
        for i, record in enumerate(records_on_db):
            assert record.zoom_url == assert_zoom_url[i]


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
        group_service.set_zoom_url(
            line_group_id=dummy_group.line_group_id,
            zoom_url="https://us01web.zoom.us/j/0123456789x?pwd=abcdefghijklmnopqrstuvwxyz",
        )

        # Assert
