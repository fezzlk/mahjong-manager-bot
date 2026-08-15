import pytest

from domain_model.entities.hanchan import Hanchan
from domain_service import (
    hanchan_service,
)
from repositories import hanchan_repository


def test_ok_add(mocker):
    # Arrange
    updated_hanchan = Hanchan(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        raw_scores={"U0123456789abcdefghijklmnopqrstu1": 1000},
    )
    mock_update_field = mocker.patch.object(
        hanchan_repository,
        "update_field",
        return_value=updated_hanchan,
    )

    # Act
    result = hanchan_service.add_or_drop_raw_score(
        999,
        "U0123456789abcdefghijklmnopqrstu1",
        1000,
    )

    # Assert
    assert result is updated_hanchan
    mock_update_field.assert_called_once_with(
        {"_id": 999},
        set_values={"raw_scores.U0123456789abcdefghijklmnopqrstu1": 1000},
    )


def test_ok_drop(mocker):
    # Arrange
    updated_hanchan = Hanchan(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        raw_scores={"U0123456789abcdefghijklmnopqrstu2": 2000},
    )
    mock_update_field = mocker.patch.object(
        hanchan_repository,
        "update_field",
        return_value=updated_hanchan,
    )

    # Act
    result = hanchan_service.add_or_drop_raw_score(
        999,
        "U0123456789abcdefghijklmnopqrstu1",
        None,
    )

    # Assert
    assert result is updated_hanchan
    mock_update_field.assert_called_once_with(
        {"_id": 999},
        unset_fields=["raw_scores.U0123456789abcdefghijklmnopqrstu1"],
    )


def test_ng_no_line_user_id(mocker):
    mock_update_field = mocker.patch.object(
        hanchan_repository,
        "update_field",
    )

    with pytest.raises(ValueError):
        hanchan_service.add_or_drop_raw_score(
            999,
            None,
            1000,
        )

    mock_update_field.assert_not_called()


def test_ng_no_hanchan(mocker):
    mock_update_field = mocker.patch.object(
        hanchan_repository,
        "update_field",
        return_value=None,
    )

    with pytest.raises(ValueError):
        hanchan_service.add_or_drop_raw_score(
            999,
            "U0123456789abcdefghijklmnopqrstu1",
            1000,
        )

    mock_update_field.assert_called_once()
