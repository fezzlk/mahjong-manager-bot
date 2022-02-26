from tests.dummies import generate_dummy_group_list
from repositories import session_scope, group_repository
from DomainModel.entities.Group import Group, GroupMode


def test_hit_1_record():
    # Arrange
    dummy_groups = generate_dummy_group_list()[:3]
    with session_scope() as session:
        for dummy_group in dummy_groups:
            group_repository.create(
                session,
                dummy_group,
            )
    target_group = dummy_groups[0]
    target_line_group_id = target_group.line_group_id

    # Act
    with session_scope() as session:
        result = group_repository.update_one_mode_by_line_group_id(
            session,
            target_line_group_id,
            mode=GroupMode.input,
        )

    # Assert
        assert isinstance(result, Group)
        assert result._id == target_group._id
        assert result.line_group_id == target_group.line_group_id
        assert result.zoom_url == target_group.zoom_url
        assert result.mode == GroupMode.input


def test_hit_0_record():
    # Arrange
    dummy_groups = generate_dummy_group_list()[1:3]
    with session_scope() as session:
        for dummy_group in dummy_groups:
            group_repository.create(
                session,
                dummy_group,
            )
    target_line_group_id = generate_dummy_group_list()[0].line_group_id

    # Act
    with session_scope() as session:
        result = group_repository.update_one_mode_by_line_group_id(
            session,
            line_group_id=target_line_group_id,
            mode=GroupMode.input,
        )

    # Assert
        assert result is None
