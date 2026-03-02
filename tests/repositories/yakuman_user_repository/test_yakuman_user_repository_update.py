from domain_model.entities.yakuman_user import YakumanUser
from repositories import yakuman_user_repository


def _make_yakuman_user(count: int = 1) -> YakumanUser:
    return YakumanUser(
        line_user_id="U_test_user_001",
        yakuman_name="大三元",
        count=count,
    )


def test_hit_1_record():
    # Arrange
    yu = _make_yakuman_user(count=1)
    yakuman_user_repository.create(yu)

    # Act
    result = yakuman_user_repository.update(
        query={"line_user_id": "U_test_user_001"},
        new_values={"count": 5},
    )

    # Assert
    assert result == 1
    records = yakuman_user_repository.find()
    assert len(records) == 1
    assert records[0].count == 5
    assert records[0].updated_at is not None


def test_hit_0_record():
    # Arrange (DB is empty)

    # Act
    result = yakuman_user_repository.update(
        query={"line_user_id": "U_nonexistent"},
        new_values={"count": 99},
    )

    # Assert
    assert result == 0
    records = yakuman_user_repository.find()
    assert len(records) == 0
