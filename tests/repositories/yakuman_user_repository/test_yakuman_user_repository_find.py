from bson.objectid import ObjectId

from domain_model.entities.yakuman_user import YakumanUser
from repositories import yakuman_user_repository


def _make_yakuman_user(suffix: str, yakuman_name: str = "大三元") -> YakumanUser:
    return YakumanUser(
        line_user_id=f"U_test_user_{suffix}",
        yakuman_name=yakuman_name,
        count=1,
    )


def test_success_find_all():
    # Arrange
    users = [_make_yakuman_user(str(i)) for i in range(3)]
    for u in users:
        yakuman_user_repository.create(u)

    # Act
    result = yakuman_user_repository.find()

    # Assert
    assert len(result) == 3
    for r in result:
        assert isinstance(r, YakumanUser)
        assert type(r._id) is ObjectId


def test_hit_0_record():
    # Arrange
    users = [_make_yakuman_user(str(i)) for i in range(2)]
    for u in users:
        yakuman_user_repository.create(u)

    # Act
    result = yakuman_user_repository.find(query={"line_user_id": "U_nonexistent"})

    # Assert
    assert len(result) == 0


def test_hit_1_record():
    # Arrange
    users = [_make_yakuman_user(str(i)) for i in range(3)]
    for u in users:
        yakuman_user_repository.create(u)
    target = users[0]

    # Act
    result = yakuman_user_repository.find(query={"line_user_id": target.line_user_id})

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], YakumanUser)
    assert result[0].line_user_id == target.line_user_id
    assert result[0].yakuman_name == target.yakuman_name


def test_find_empty_collection():
    # Act
    result = yakuman_user_repository.find()

    # Assert
    assert result == []
