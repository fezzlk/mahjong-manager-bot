from DomainModel.entities.Group import Group, GroupMode
from repositories import group_repository

before = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.wait.value,
)

after = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu2",
    mode=GroupMode.wait.value,
)


def test_hit_1_record():
    # Arrange
    group_repository.create(before)

    # Act
    result = group_repository.update(
        query={'line_group_id': before.line_group_id},
        new_values={'line_group_id': after.line_group_id},
    )

    # Assert
    assert result == 1
    record_on_db = group_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_group_id == after.line_group_id
    assert record_on_db[0].mode == after.mode


def test_hit_0_record():
    # Arrange

    # Act
    result = group_repository.update(
        query={},
        new_values={'line_group_id': after.line_group_id},
    )

    # Assert
    assert result == 0
