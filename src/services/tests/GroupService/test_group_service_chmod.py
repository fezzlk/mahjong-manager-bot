from domains.entities.Group import GroupMode
from services.GroupService import GroupService
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
    assert_modes = [GroupMode.input, GroupMode.wait, GroupMode.wait]

    # Act
    result = group_service.chmod(
        line_group_id=dummy_group.line_group_id,
        mode=GroupMode.input,
    )

    # Assert
    assert result.mode == GroupMode.input
    with session_scope() as session:
        records_on_db = group_repository.find_all(session)
        for i, record in enumerate(records_on_db):
            assert record.mode == assert_modes[i]


def test_not_hit():
    # Arrange
    group_service = GroupService()
    dummy_groups = generate_dummy_group_list()[:3]
    dummy_group = dummy_groups[0]
    with session_scope() as session:
        for record in dummy_groups[1:]:
            group_repository.create(session, record)

    # Act
    result = group_service.chmod(
        line_group_id=dummy_group.line_group_id,
        mode=GroupMode.input,
    )

    # Assert
    assert result is None
