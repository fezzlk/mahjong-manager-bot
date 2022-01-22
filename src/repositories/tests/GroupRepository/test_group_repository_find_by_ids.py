from tests.dummies import generate_dummy_group_list
from Repositories import session_scope, group_repository
from Domains.Entities.Group import Group


def test_hit_with_ids():
    # Arrange
    with session_scope() as session:
        dummy_groups = generate_dummy_group_list()[:3]
        for dummy_group in dummy_groups:
            group_repository.create(
                session,
                dummy_group,
            )
    target_groups = generate_dummy_group_list()[1:3]
    ids = [target_group._id for target_group in target_groups]

    # Act
    with session_scope() as session:
        result = group_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == len(target_groups)
        for i in range(len(result)):
            assert isinstance(result[i], Group)
            assert result[i]._id == target_groups[i]._id
            assert result[i].line_group_id == target_groups[i].line_group_id
            assert result[i].zoom_url == target_groups[i].zoom_url
            assert result[i].mode == target_groups[i].mode


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_groups = generate_dummy_group_list()[:3]
        for dummy_group in dummy_groups:
            group_repository.create(
                session,
                dummy_group,
            )
    target_groups = generate_dummy_group_list()[3:6]
    ids = [target_group._id for target_group in target_groups]

    # Act
    with session_scope() as session:
        result = group_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == 0
