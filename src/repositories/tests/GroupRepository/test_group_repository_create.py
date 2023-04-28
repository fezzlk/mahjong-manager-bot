from DomainModel.entities.Group import Group
from tests.dummies import generate_dummy_group_list
from repositories import group_repository


def test_success():
    # Arrange
    dummy_group = generate_dummy_group_list()[0]

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
    assert record_on_db[0]._id == dummy_group._id
    assert record_on_db[0].line_group_id == dummy_group.line_group_id
    assert record_on_db[0].mode == dummy_group.mode
