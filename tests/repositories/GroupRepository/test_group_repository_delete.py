from repositories import group_repository
from dummies import generate_dummy_group_list


def test_hit_with_ids():
    # Arrange
    dummy_groups = generate_dummy_group_list()[:3]
    for dummy_group in dummy_groups:
        group_repository.create(
            dummy_group,
        )
    other_groups = dummy_groups[:1]
    target_groups = dummy_groups[1:3]
    ids = [target_group._id for target_group in target_groups]

    # Act
    result = group_repository.delete(
        query={"_id": {"$in": ids}},
    )

    # Assert
    assert result == len(target_groups)
    record_on_db = group_repository.find()
    assert len(record_on_db) == len(other_groups)
    for i in range(len(record_on_db)):
        assert record_on_db[i].line_group_id == other_groups[i].line_group_id
        assert record_on_db[i].mode == other_groups[i].mode


def test_hit_0_record():
    # Arrange
    dummy_groups = generate_dummy_group_list()[:3]
    for dummy_group in dummy_groups:
        group_repository.create(
            dummy_group,
        )
    target_groups = generate_dummy_group_list()[3:6]
    ids = [target_group._id for target_group in target_groups]

    # Act
    result = group_repository.delete(
        query={"_id": {"$in": ids}},
    )

    # Assert
    assert result == 0
    record_on_db = group_repository.find()
    assert len(record_on_db) == len(dummy_groups)
    for i in range(len(record_on_db)):
        assert record_on_db[i].line_group_id == dummy_groups[i].line_group_id
        assert record_on_db[i].mode == dummy_groups[i].mode
