from DomainModel.entities.UserMatch import UserMatch
from repositories import user_match_repository
from datetime import datetime

before = UserMatch(
    user_id='U0123456789abcdefghijklmnopqrstu3',
    match_id=1,
    created_at=datetime(2022,1, 2, 3, 4, 5),
    updated_at=datetime(2023,1, 2, 3, 4, 5),
)

after = UserMatch(
    user_id='U0123456789abcdefghijklmnopqrstu3',
    match_id=1,
    created_at=datetime(2021,1, 2, 3, 4, 5),
    updated_at=datetime(2023,1, 2, 3, 4, 5),
)


def test_hit_1_record():
    # Arrange
    user_match_repository.create(before)

    # Act
    result = user_match_repository.update(
        query={'match_id': before.match_id},
        new_values={
            'created_at': after.created_at,
            'updated_at': after.updated_at,
        },
    )

    # Assert
    assert result == 1
    record_on_db = user_match_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].user_id == after.user_id
    assert record_on_db[0].match_id == after.match_id
    assert record_on_db[0].created_at == after.created_at
    assert record_on_db[0].updated_at != after.updated_at


def test_hit_0_record():
    # Arrange

    # Act
    result = user_match_repository.update(
        query={},
        new_values={'match_id': after.match_id},
    )

    # Assert
    assert result == 0
