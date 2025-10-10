import pytest
from bson.objectid import ObjectId

from DomainModel.entities.Group import Group, GroupMode
from repositories import group_repository
from dummies import generate_dummy_group_list


def test_success():
    # Arrange
    dummy_group = generate_dummy_group_list()[0]

    # Act
    result = group_repository.create(
        dummy_group,
    )

    # Assert
    assert isinstance(result, Group)
    assert type(result._id) is ObjectId
    assert result.line_group_id == dummy_group.line_group_id
    assert result.mode == dummy_group.mode

    record_on_db = group_repository.find()

    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) is ObjectId
    assert record_on_db[0].line_group_id == dummy_group.line_group_id
    assert record_on_db[0].mode == dummy_group.mode


def test_success_with_id():
    # Arrange
    dummy_group = Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        mode=GroupMode.wait.value,
        _id=ObjectId("644c838186bbd9e20a91b783"),
    )
    # Act
    result = group_repository.create(
        dummy_group,
    )

    # Assert
    assert isinstance(result, Group)
    assert result._id == dummy_group._id
    assert result.line_group_id == dummy_group.line_group_id
    assert result.mode == dummy_group.mode

    record_on_db = group_repository.find()

    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) is ObjectId
    assert record_on_db[0].line_group_id == dummy_group.line_group_id
    assert record_on_db[0].mode == dummy_group.mode


def test_fail_duplicate_line_group_id():
    with pytest.raises(Exception):
        # Arrange
        dummy_groups = [
            Group(
                line_group_id="G0123456789abcdefghijklmnopqrstu2",
                mode=GroupMode.wait.value,
            ),
            Group(
                line_group_id="G0123456789abcdefghijklmnopqrstu2",
                mode=GroupMode.wait.value,
            ),
        ]

        group_repository.create(
            dummy_groups[0],
        )

        # Act
        group_repository.create(
            dummy_groups[1],
        )

    # Assert
    record_on_db = group_repository.find()
    assert len(record_on_db) == 1
