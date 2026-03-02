from datetime import datetime

from bson.objectid import ObjectId

from domain_model.entities.yakuman_user import YakumanUser


def test_success():
    # Arrange
    oid = ObjectId()

    # Act
    yu = YakumanUser(
        _id=oid,
        line_user_id="U_test_user_001",
        yakuman_name="大三元",
        count=3,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
    )

    # Assert
    assert yu._id == oid
    assert yu.line_user_id == "U_test_user_001"
    assert yu.yakuman_name == "大三元"
    assert yu.count == 3
    assert yu.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert yu.updated_at == datetime(2023, 1, 2, 3, 4, 5)


def test_success_default():
    # Act
    yu = YakumanUser()

    # Assert
    assert yu._id is None
    assert yu.line_user_id is None
    assert yu.yakuman_name is None
    assert yu.count is None
    assert yu.created_at is None
    assert yu.updated_at is None


def test_setitem():
    """__setitem__ による属性設定が正常に機能する"""
    yu = YakumanUser()
    yu["line_user_id"] = "U_setitem_test"
    yu["yakuman_name"] = "四暗刻"
    yu["count"] = 1

    assert yu.line_user_id == "U_setitem_test"
    assert yu.yakuman_name == "四暗刻"
    assert yu.count == 1
