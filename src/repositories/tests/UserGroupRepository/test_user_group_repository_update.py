from DomainModel.entities.UserGroup import UserGroup
from repositories import user_group_repository
from datetime import datetime

before = UserGroup(
    line_user_id='U0123456789abcdefghijklmnopqrstu3',
    line_group_id='G0123456789abcdefghijklmnopqrstu3',
    created_at=datetime(2022,1, 2, 3, 4, 5),
    updated_at=datetime(2023,1, 2, 3, 4, 5),
)

after = UserGroup(
    line_user_id='U0123456789abcdefghijklmnopqrstu3',
    line_group_id='G0123456789abcdefghijklmnopqrstu3',
    created_at=datetime(2021,1, 2, 3, 4, 5),
    updated_at=datetime(2023,1, 2, 3, 4, 5),
)


def test_hit_1_record():
    # Arrange
    user_group_repository.create(before)

    # Act
    result = user_group_repository.update(
        query={'line_group_id': before.line_group_id},
        new_values={
            'created_at': after.created_at,
            'updated_at': after.updated_at,
        },
    )

    # Assert
    assert result == 1
    record_on_db = user_group_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_user_id == after.line_user_id
    assert record_on_db[0].line_group_id == after.line_group_id
    assert record_on_db[0].created_at == after.created_at
    assert record_on_db[0].updated_at != after.updated_at


def test_hit_0_record():
    # Arrange

    # Act
    result = user_group_repository.update(
        query={},
        new_values={'line_group_id': after.line_group_id},
    )

    # Assert
    assert result == 0
