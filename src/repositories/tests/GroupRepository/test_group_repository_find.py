from bson.objectid import ObjectId

from DomainModel.entities.Group import Group
from repositories import group_repository
from tests.dummies import generate_dummy_group_list


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
        assert type(result[i]._id) == ObjectId
        assert result[i].line_group_id == dummy_groups[i].line_group_id
        assert result[i].mode == dummy_groups[i].mode


def test_hit_0_record():
    # Arrange
    dummy_groups = generate_dummy_group_list()[:2]
    for dummy_group in dummy_groups:
        group_repository.create(
            dummy_group,
        )
    target_group = generate_dummy_group_list()[2]

    # Act
    result = group_repository.find(
        query={"line_group_id": target_group.line_group_id},
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
        query={"line_group_id": target_line_group_id},
    )

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], Group)
    assert type(result[0]._id) == ObjectId
    assert result[0].line_group_id == target_group.line_group_id
    assert result[0].mode == target_group.mode
