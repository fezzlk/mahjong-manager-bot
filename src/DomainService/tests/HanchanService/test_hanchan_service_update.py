from datetime import datetime

from DomainModel.entities.Hanchan import Hanchan
from DomainService import (
    hanchan_service,
)
from repositories import hanchan_repository

dummy_hanchans = [
    Hanchan(
        _id=1,
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
    ),
]


def test_ok_hit_hanchan(mocker):
    # Arrange
    mock_update = mocker.patch.object(
        hanchan_repository,
        "update",
        return_value=1,
    )

    # Act
    hanchan_service.update(dummy_hanchans[0])

    # Assert
    mock_update.assert_called_once_with({"_id": 1}, {"_id": 1, "line_group_id": "G0123456789abcdefghijklmnopqrstu1", "raw_scores": {}, "converted_scores": {}, "match_id": 1, "status": 2, "original_id": None, "created_at": datetime(2022, 1, 2, 3, 4, 5), "updated_at": datetime(2023, 1, 2, 3, 4, 5)})
