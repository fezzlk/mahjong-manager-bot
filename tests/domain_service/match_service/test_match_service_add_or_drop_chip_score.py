import pytest

from domain_model.entities.match import Match
from domain_service import (
    match_service,
)
from repositories import match_repository


def test_ok_add(mocker):
    # Arrange
    updated_match = Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        chip_scores={"U0123456789abcdefghijklmnopqrstu1": 10},
    )
    mock_update_field = mocker.patch.object(
        match_repository,
        "update_field",
        return_value=updated_match,
    )

    # Act
    result = match_service.add_or_drop_chip_score(
        999,
        "U0123456789abcdefghijklmnopqrstu1",
        10,
    )

    # Assert
    assert result is updated_match
    mock_update_field.assert_called_once_with(
        {"_id": 999},
        set_values={"chip_scores.U0123456789abcdefghijklmnopqrstu1": 10},
    )


def test_ok_drop(mocker):
    # Arrange
    updated_match = Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        chip_scores={},
    )
    mock_update_field = mocker.patch.object(
        match_repository,
        "update_field",
        return_value=updated_match,
    )

    # Act
    result = match_service.add_or_drop_chip_score(
        999,
        "U0123456789abcdefghijklmnopqrstu1",
        None,
    )

    # Assert
    assert result is updated_match
    mock_update_field.assert_called_once_with(
        {"_id": 999},
        unset_fields=["chip_scores.U0123456789abcdefghijklmnopqrstu1"],
    )


def test_ng_no_line_user_id(mocker):
    mock_update_field = mocker.patch.object(
        match_repository,
        "update_field",
    )

    with pytest.raises(ValueError):
        match_service.add_or_drop_chip_score(
            999,
            None,
            10,
        )

    mock_update_field.assert_not_called()


def test_ng_no_match(mocker):
    mock_update_field = mocker.patch.object(
        match_repository,
        "update_field",
        return_value=None,
    )

    with pytest.raises(ValueError):
        match_service.add_or_drop_chip_score(
            999,
            "U0123456789abcdefghijklmnopqrstu1",
            10,
        )

    mock_update_field.assert_called_once()
