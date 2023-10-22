from DomainService import (
    hanchan_service,
)
from repositories import hanchan_repository
from DomainModel.entities.Hanchan import Hanchan

dummy_hanchans = [
    Hanchan(
        _id=1,
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
    )
]


def test_ok_hit_hanchan(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=dummy_hanchans,
    )

    # Act
    result = hanchan_service.find_one_by_id(1)

    # Assert
    assert isinstance(result, Hanchan)
    assert result.match_id == 1
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert result.status == 2
    mock_find.assert_called_once_with({'_id': 1})



def test_no_hit(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=[],
    )

    # Act
    result = hanchan_service.find_one_by_id(1)

    # Assert
    assert result is None
    mock_find.assert_called_once_with({'_id': 1})
