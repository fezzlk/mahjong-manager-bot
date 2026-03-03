from datetime import datetime

from bson.objectid import ObjectId

from domain_model.entities.hanchan import Hanchan
from domain_model.entities.user_hanchan import UserHanchanResult
from domain_service import user_hanchan_service
from repositories import hanchan_repository

dummy_hanchan_id = ObjectId("000000000000000000000001")

dummy_hanchan = Hanchan(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    match_id=1,
    results=[
        UserHanchanResult(line_user_id="U0123456789abcdefghijklmnopqrstu1", rank=4, point=1000),
    ],
    _id=dummy_hanchan_id,
    created_at=datetime(2022, 1, 2, 3, 4, 5),
)


def test_ok_with_no_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        hanchan_repository,
        "find",
        return_value=[dummy_hanchan],
    )

    # Act
    result = user_hanchan_service.find_all_each_line_user_id(["U0123456789abcdefghijklmnopqrstu1"])

    # Assert
    assert len(result) == 1
    assert result[0].line_user_id == "U0123456789abcdefghijklmnopqrstu1"
    assert result[0].hanchan_id == dummy_hanchan_id
    assert result[0].point == 1000
    assert result[0].rank == 4
    mock_find.assert_called_once_with(
        query={"$and": [{"results": {"$elemMatch": {"line_user_id": {"$in": ["U0123456789abcdefghijklmnopqrstu1"]}}}}]},
        sort=[("_id", 1)],
    )


def test_ok_with_from_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        hanchan_repository,
        "find",
        return_value=[dummy_hanchan],
    )

    # Act
    result = user_hanchan_service.find_all_each_line_user_id(
        ["U0123456789abcdefghijklmnopqrstu1"],
        from_dt=datetime(2022, 1, 2, 3, 4, 5),
    )

    # Assert
    assert len(result) == 1
    mock_find.assert_called_once_with(
        query={"$and": [
            {"results": {"$elemMatch": {"line_user_id": {"$in": ["U0123456789abcdefghijklmnopqrstu1"]}}}},
            {"created_at": {"$gte": datetime(2022, 1, 2, 3, 4, 5)}},
        ]},
        sort=[("_id", 1)],
    )


def test_ok_with_to_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        hanchan_repository,
        "find",
        return_value=[dummy_hanchan],
    )

    # Act
    result = user_hanchan_service.find_all_each_line_user_id(
        ["U0123456789abcdefghijklmnopqrstu1"],
        to_dt=datetime(2022, 1, 2, 3, 4, 5),
    )

    # Assert
    assert len(result) == 1
    mock_find.assert_called_once_with(
        query={"$and": [
            {"results": {"$elemMatch": {"line_user_id": {"$in": ["U0123456789abcdefghijklmnopqrstu1"]}}}},
            {"created_at": {"$lte": datetime(2022, 1, 2, 3, 4, 5)}},
        ]},
        sort=[("_id", 1)],
    )


def test_ok_with_both_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        hanchan_repository,
        "find",
        return_value=[dummy_hanchan],
    )

    # Act
    result = user_hanchan_service.find_all_each_line_user_id(
        ["U0123456789abcdefghijklmnopqrstu1"],
        from_dt=datetime(2022, 1, 2, 3, 4, 5),
        to_dt=datetime(2023, 1, 2, 3, 4, 5),
    )

    # Assert
    assert len(result) == 1
    mock_find.assert_called_once_with(
        query={"$and": [
            {"results": {"$elemMatch": {"line_user_id": {"$in": ["U0123456789abcdefghijklmnopqrstu1"]}}}},
            {"created_at": {"$gte": datetime(2022, 1, 2, 3, 4, 5)}},
            {"created_at": {"$lte": datetime(2023, 1, 2, 3, 4, 5)}},
        ]},
        sort=[("_id", 1)],
    )
