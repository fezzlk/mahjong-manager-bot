from bson.objectid import ObjectId

from domain_model.entities.yakuman_user import YakumanUser
from repositories import yakuman_user_repository


def _make_yakuman_user(suffix: str = "001") -> YakumanUser:
    return YakumanUser(
        line_user_id=f"U_test_user_{suffix}",
        yakuman_name="大三元",
        count=1,
    )


def test_success():
    # Arrange
    yu = _make_yakuman_user("001")

    # Act
    result = yakuman_user_repository.create(yu)

    # Assert
    assert isinstance(result, YakumanUser)
    assert type(result._id) is ObjectId
    assert result.line_user_id == yu.line_user_id
    assert result.yakuman_name == yu.yakuman_name

    records = yakuman_user_repository.find()
    assert len(records) == 1
    assert records[0].line_user_id == yu.line_user_id


def test_success_always_pops_id():
    """create() は常に _id を MongoDB に採番させる (指定した _id は無視される)"""
    oid = ObjectId("644c838186bbd9e20a91b783")
    yu = _make_yakuman_user("002")
    yu._id = oid

    result = yakuman_user_repository.create(yu)

    # _id は MongoDB が採番した新しい ObjectId になる
    assert type(result._id) is ObjectId
    records = yakuman_user_repository.find()
    assert len(records) == 1
    # created_at が自動設定されている
    assert records[0].created_at is not None
