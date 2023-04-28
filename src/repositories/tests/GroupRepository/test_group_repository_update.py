from DomainModel.entities.Group import Group, GroupMode
from repositories import group_repository
from tests.dummies import generate_dummy_group_list

before = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.wait.value,
    _id=1,
)

after = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu2",
    mode=GroupMode.wait.value,
    _id=1,
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
    assert record_on_db[0]._id == after._id
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


def test_update_mode():
    # Arrange
    dummy_groups = generate_dummy_group_list()[:3]
    for dummy_group in dummy_groups:
        group_repository.create(
            dummy_group,
        )       
    target_group = dummy_groups[0]
    target_line_group_id = target_group.line_group_id

    # Act
    result = group_repository.update(
        query={'line_group_id': target_line_group_id},
        new_values={'mode': GroupMode.input.value},
    )

    # Assert
    assert result == 1
