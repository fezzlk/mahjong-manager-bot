from tests.dummies import generate_dummy_group_list
from repositories import group_repository
from DomainModel.entities.Group import Group


def test_success_find_records():
    # Arrange
    dummy_groups = generate_dummy_group_list()[:3]
    for dummy_group in dummy_groups:
        group_repository.create(
            dummy_group,
        )

    # Act
    result = group_repository.find()

    # Assert
    assert len(result) == len(dummy_groups)
    for i in range(len(result)):
        assert isinstance(result[i], Group)
        assert result[i]._id == dummy_groups[i]._id
        assert result[i].line_group_id == dummy_groups[i].line_group_id
        assert result[i].mode == dummy_groups[i].mode


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    result = group_repository.find()

    # Assert
    assert len(result) == 0


def test_hit_with_ids():
    # Arrange
    dummy_groups = generate_dummy_group_list()[:3]
    for dummy_group in dummy_groups:
        group_repository.create(
            dummy_group,
        )
    target_groups = generate_dummy_group_list()[1:3]
    ids = [target_group._id for target_group in target_groups]

    # Act
    result = group_repository.find(
        query={'_id': {'$in': ids}},
    )

    # Assert
    assert len(result) == len(target_groups)
    for i in range(len(result)):
        assert isinstance(result[i], Group)
        assert result[i]._id == target_groups[i]._id
        assert result[i].line_group_id == target_groups[i].line_group_id
        assert result[i].mode == target_groups[i].mode


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
    result = group_repository.find(
        query={'_id': {'$in': ids}},
    )

    # Assert
    assert len(result) == 0


def test_hit_1_record():
    # Arrange
    dummy_groups = generate_dummy_group_list()[:3]
    for dummy_group in dummy_groups:
        group_repository.create(
            dummy_group,
        )
    target_group = dummy_groups[0]
    target_line_group_id = target_group.line_group_id

    # Act
    result = group_repository.find(
        query={'line_group_id': target_line_group_id},
    )

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], Group)
    assert result[0]._id == target_group._id
    assert result[0].line_group_id == target_group.line_group_id
    assert result[0].mode == target_group.mode


def test_hit_0_record_with_line_group_id():
    # Arrange
    dummy_groups = generate_dummy_group_list()[1:3]
    for dummy_group in dummy_groups:
        group_repository.create(
            dummy_group,
        )
    target_line_group_id = generate_dummy_group_list()[0].line_group_id

    # Act
    result = group_repository.find(
        query={'line_group_id': target_line_group_id},
    )

    # Assert
    assert len(result) == 0
