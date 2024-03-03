from DomainModel.entities.UserHanchan import UserHanchan
from repositories import user_hanchan_repository
from datetime import datetime

before = UserHanchan(
    line_user_id='U0123456789abcdefghijklmnopqrstu3',
    hanchan_id=1,
    point=10000,
    rank=4,
    yakuman_count=False,
    created_at=datetime(2022,1, 2, 3, 4, 5),
    updated_at=datetime(2023,1, 2, 3, 4, 5),
)

after = UserHanchan(
    line_user_id='U0123456789abcdefghijklmnopqrstu3',
    hanchan_id=1,
    point=10000,
    rank=4,
    yakuman_count=True,
    created_at=datetime(2022,1, 2, 3, 4, 5),
    updated_at=datetime(2023,1, 2, 3, 4, 5),
)



def test_hit_1_record():
    # Arrange
    user_hanchan_repository.create(before)

    # Act
    result = user_hanchan_repository.update(
        query={'hanchan_id': before.hanchan_id},
        new_values={
            'yakuman_count': after.yakuman_count,
            'updated_at': after.updated_at,
        },
    )

    # Assert
    assert result == 1
    record_on_db = user_hanchan_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_user_id == after.line_user_id
    assert record_on_db[0].hanchan_id == after.hanchan_id
    assert record_on_db[0].point == after.point
    assert record_on_db[0].rank == after.rank
    assert record_on_db[0].yakuman_count == after.yakuman_count
    assert record_on_db[0].created_at == after.created_at
    assert record_on_db[0].updated_at != after.updated_at


def test_hit_0_record():
    # Arrange

    # Act
    result = user_hanchan_repository.update(
        query={},
        new_values={'hanchan_id': after.hanchan_id},
    )

    # Assert
    assert result == 0
