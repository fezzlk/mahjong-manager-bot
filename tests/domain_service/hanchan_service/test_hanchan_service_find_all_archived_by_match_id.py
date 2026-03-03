from pymongo import ASCENDING

from domain_model.entities.hanchan import Hanchan
from domain_service import (
    hanchan_service,
)
from repositories import hanchan_repository

dummy_hanchans = [
    Hanchan(
        _id=1,
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    ),
    Hanchan(
        _id=2,
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    ),
]


def test_ok_hit_hanchan(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        hanchan_repository,
        "find",
        return_value=dummy_hanchans,
    )

    # Act
    result = hanchan_service.find_all_archived_by_match_id(1)

    # Assert
    assert len(result) == len(dummy_hanchans)
    for i, _item in enumerate(dummy_hanchans):
        assert isinstance(result[i], Hanchan)
        assert result[i]._id == dummy_hanchans[i]._id
        assert result[i].match_id == dummy_hanchans[i].match_id
        assert result[i].line_group_id == dummy_hanchans[i].line_group_id
        assert result[i].is_deleted == dummy_hanchans[i].is_deleted
    mock_find.assert_called_once_with({"match_id": 1, "converted_scores": {"$ne": {}}}, [("_id", ASCENDING)])
