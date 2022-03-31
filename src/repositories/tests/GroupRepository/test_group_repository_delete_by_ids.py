from tests.dummies import generate_dummy_group_list
from repositories import session_scope, group_repository
from DomainModel.entities.Group import Group


def test_hit_with_ids():
    # Arrange
    dummy_groups = generate_dummy_group_list()[:3]
    with session_scope() as session:
        for dummy_group in dummy_groups:
            group_repository.create(
                session,
                dummy_group,
            )
    other_groups = dummy_groups[:1]
    target_groups = dummy_groups[1:3]
    ids = [target_group._id for target_group in target_groups]

    # Act
    with session_scope() as session:
        result = group_repository.delete_by_ids(
            session,
            ids,
        )

    # Assert
    assert result == len(target_groups)
    with session_scope() as session:
        record_on_db = group_repository.find_all(
            session,
        )
        assert len(record_on_db) == len(other_groups)
        for i in range(len(record_on_db)):
            assert isinstance(record_on_db[i], Group)
            assert record_on_db[i].line_group_id == other_groups[i].line_group_id
            assert record_on_db[i].zoom_url == other_groups[i].zoom_url
            assert record_on_db[i].mode == other_groups[i].mode


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
        result = group_repository.delete_by_ids(
            session,
            ids,
        )

    # Assert
    assert result == 0
    with session_scope() as session:
        record_on_db = group_repository.find_all(
            session,
        )
        assert len(record_on_db) == len(dummy_groups)
        for i in range(len(record_on_db)):
            assert isinstance(record_on_db[i], Group)
            assert record_on_db[i].line_group_id == dummy_groups[i].line_group_id
            assert record_on_db[i].zoom_url == dummy_groups[i].zoom_url
            assert record_on_db[i].mode == dummy_groups[i].mode
