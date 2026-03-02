import pytest

from domain_model.entities.yakuman_user import YakumanUser
from repositories import yakuman_user_repository


def _make_yakuman_user(suffix: str) -> YakumanUser:
    return YakumanUser(
        line_user_id=f"U_test_user_{suffix}",
        yakuman_name="四暗刻",
        count=1,
    )


def test_hit_1_record():
    # Arrange
    users = [_make_yakuman_user(str(i)) for i in range(3)]
    for u in users:
        yakuman_user_repository.create(u)
    target = users[0]

    # Act
    result = yakuman_user_repository.delete(
        query={"line_user_id": target.line_user_id},
    )

    # Assert
    assert result == 1
    records = yakuman_user_repository.find()
    assert len(records) == 2
    remaining_ids = [r.line_user_id for r in records]
    assert target.line_user_id not in remaining_ids


def test_hit_0_record():
    # Arrange
    users = [_make_yakuman_user(str(i)) for i in range(2)]
    for u in users:
        yakuman_user_repository.create(u)

    # Act
    result = yakuman_user_repository.delete(
        query={"line_user_id": "U_nonexistent"},
    )

    # Assert
    assert result == 0
    records = yakuman_user_repository.find()
    assert len(records) == 2


def test_fail_empty_query():
    """空クエリは ValueError を発生させる"""
    with pytest.raises(ValueError):
        yakuman_user_repository.delete(query={})


def test_fail_none_query():
    """None クエリは ValueError を発生させる"""
    with pytest.raises(ValueError):
        yakuman_user_repository.delete(query=None)
