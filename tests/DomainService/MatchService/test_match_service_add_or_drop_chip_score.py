import pytest

from DomainModel.entities.Match import Match
from DomainService import (
    match_service,
)
from repositories import match_repository

dummy_matches1 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        chip_scores={},
    ),
]


def test_ok_add_init(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        "find",
        return_value=dummy_matches1,
    )
    mock_update = mocker.patch.object(
        match_repository,
        "update",
    )

    # Act
    result = match_service.add_or_drop_chip_score(
        "G0123456789abcdefghijklmnopqrstu1",
        "U0123456789abcdefghijklmnopqrstu1",
        10,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.chip_scores) == 1
    assert result.chip_scores["U0123456789abcdefghijklmnopqrstu1"] == 10
    mock_update.assert_called_once()


dummy_matches2 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        chip_scores={"U0123456789abcdefghijklmnopqrstu2": 20},
    ),
]


def test_ok_add_second(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        "find",
        return_value=dummy_matches2,
    )
    mock_update = mocker.patch.object(
        match_repository,
        "update",
    )

    # Act
    result = match_service.add_or_drop_chip_score(
        "G0123456789abcdefghijklmnopqrstu1",
        "U0123456789abcdefghijklmnopqrstu1",
        10,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.chip_scores) == 2
    assert result.chip_scores["U0123456789abcdefghijklmnopqrstu2"] == 20
    assert result.chip_scores["U0123456789abcdefghijklmnopqrstu1"] == 10
    mock_update.assert_called_once()


dummy_matches3 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        chip_scores={
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu1": 30,
        },
    ),
]


def test_ok_update(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        "find",
        return_value=dummy_matches3,
    )
    mock_update = mocker.patch.object(
        match_repository,
        "update",
    )

    # Act
    result = match_service.add_or_drop_chip_score(
        "G0123456789abcdefghijklmnopqrstu1",
        "U0123456789abcdefghijklmnopqrstu1",
        10,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.chip_scores) == 2
    assert result.chip_scores["U0123456789abcdefghijklmnopqrstu2"] == 20
    assert result.chip_scores["U0123456789abcdefghijklmnopqrstu1"] == 10
    mock_update.assert_called_once()


dummy_matches3 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        chip_scores={
            "U0123456789abcdefghijklmnopqrstu2": 20,
            "U0123456789abcdefghijklmnopqrstu1": 30,
        },
    ),
]


def test_ok_drop(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        "find",
        return_value=dummy_matches3,
    )
    mock_update = mocker.patch.object(
        match_repository,
        "update",
    )

    # Act
    result = match_service.add_or_drop_chip_score(
        "G0123456789abcdefghijklmnopqrstu1",
        "U0123456789abcdefghijklmnopqrstu1",
        None,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.chip_scores) == 1
    assert result.chip_scores["U0123456789abcdefghijklmnopqrstu2"] == 20
    mock_update.assert_called_once()


dummy_matches4 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
        chip_scores={
            "U0123456789abcdefghijklmnopqrstu1": 30,
        },
    ),
]


def test_ok_drop_all(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        "find",
        return_value=dummy_matches4,
    )
    mock_update = mocker.patch.object(
        match_repository,
        "update",
    )

    # Act
    result = match_service.add_or_drop_chip_score(
        999,
        "U0123456789abcdefghijklmnopqrstu1",
        None,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.chip_scores) == 0
    mock_update.assert_called_once()


def test_ng_no_line_user_id(mocker):
    with pytest.raises(ValueError):
        # Arrange
        mock_find = mocker.patch.object(
            match_repository,
            "find",
        )
        mock_update = mocker.patch.object(
            match_repository,
            "update",
        )

        # Act
        match_service.add_or_drop_chip_score(
            "G0123456789abcdefghijklmnopqrstu1",
            None,
            10,
        )

    # Assert
    mock_find.assert_not_called()
    mock_update.assert_not_called()


def test_ng_no_hanchan(mocker):
    with pytest.raises(ValueError):
        # Arrange
        mocker.patch.object(
            match_repository,
            "find",
            return_value=[],
        )
        mock_update = mocker.patch.object(
            match_repository,
            "update",
        )

        # Act
        match_service.add_or_drop_chip_score(
            "G0123456789abcdefghijklmnopqrstu1",
            "U0123456789abcdefghijklmnopqrstu1",
            10,
        )

    # Assert
    mock_update.assert_not_called()
