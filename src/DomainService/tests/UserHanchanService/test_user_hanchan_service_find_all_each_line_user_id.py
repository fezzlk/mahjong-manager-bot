from DomainService import (
    user_hanchan_service,
)
from repositories import user_hanchan_repository
from DomainModel.entities.UserHanchan import UserHanchan
from datetime import datetime


dummy_user_hanchan = UserHanchan(
        _id=1,
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        hanchan_id=1,
        point=1000,
        rank=4,
    )


def test_ok_with_no_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_hanchan_repository,
        'find',
        return_value=[dummy_user_hanchan],
    )

    # Act
    result = user_hanchan_service.find_all_each_line_user_id("G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert len(result) == 1
    assert result[0]._id == dummy_user_hanchan._id
    assert result[0].line_user_id == dummy_user_hanchan.line_user_id
    assert result[0].hanchan_id == dummy_user_hanchan.hanchan_id
    assert result[0].point == dummy_user_hanchan.point
    assert result[0].rank == dummy_user_hanchan.rank
    mock_find.assert_called_once_with(query={'$and': [{'line_user_id': {'$in': 'G0123456789abcdefghijklmnopqrstu1'}}]}, sort=[('hanchan_id', 1)])


def test_ok_with_from_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_hanchan_repository,
        'find',
        return_value=[dummy_user_hanchan],
    )

    # Act
    result = user_hanchan_service.find_all_each_line_user_id("G0123456789abcdefghijklmnopqrstu1", from_dt=datetime(2022,1,2,3,4,5))

    # Assert
    assert len(result) == 1
    assert result[0]._id == dummy_user_hanchan._id
    assert result[0].line_user_id == dummy_user_hanchan.line_user_id
    assert result[0].hanchan_id == dummy_user_hanchan.hanchan_id
    assert result[0].point == dummy_user_hanchan.point
    assert result[0].rank == dummy_user_hanchan.rank
    mock_find.assert_called_once_with(query={'$and': [{'line_user_id': {'$in': 'G0123456789abcdefghijklmnopqrstu1'}}, {'created_at': {'$gte': datetime(2022, 1, 2, 3, 4, 5)}}]}, sort=[('hanchan_id', 1)])


def test_ok_with_to_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_hanchan_repository,
        'find',
        return_value=[dummy_user_hanchan],
    )

    # Act
    result = user_hanchan_service.find_all_each_line_user_id("G0123456789abcdefghijklmnopqrstu1", to_dt=datetime(2022,1,2,3,4,5))

    # Assert
    assert len(result) == 1
    assert result[0]._id == dummy_user_hanchan._id
    assert result[0].line_user_id == dummy_user_hanchan.line_user_id
    assert result[0].hanchan_id == dummy_user_hanchan.hanchan_id
    assert result[0].point == dummy_user_hanchan.point
    assert result[0].rank == dummy_user_hanchan.rank
    mock_find.assert_called_once_with(query={'$and': [{'line_user_id': {'$in': 'G0123456789abcdefghijklmnopqrstu1'}}, {'created_at': {'$lte': datetime(2022, 1, 2, 3, 4, 5)}}]}, sort=[('hanchan_id', 1)])


def test_ok_with_both_query(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        user_hanchan_repository,
        'find',
        return_value=[dummy_user_hanchan],
    )

    # Act
    result = user_hanchan_service.find_all_each_line_user_id("G0123456789abcdefghijklmnopqrstu1", from_dt=datetime(2022,1,2,3,4,5), to_dt=datetime(2023,1,2,3,4,5))

    # Assert
    assert len(result) == 1
    assert result[0]._id == dummy_user_hanchan._id
    assert result[0].line_user_id == dummy_user_hanchan.line_user_id
    assert result[0].hanchan_id == dummy_user_hanchan.hanchan_id
    assert result[0].point == dummy_user_hanchan.point
    assert result[0].rank == dummy_user_hanchan.rank
    mock_find.assert_called_once_with(query={'$and': [{'line_user_id': {'$in': 'G0123456789abcdefghijklmnopqrstu1'}}, {'created_at': {'$gte': datetime(2022, 1, 2, 3, 4, 5)}}, {'created_at': {'$lte': datetime(2023, 1, 2, 3, 4, 5)}}]}, sort=[('hanchan_id', 1)])