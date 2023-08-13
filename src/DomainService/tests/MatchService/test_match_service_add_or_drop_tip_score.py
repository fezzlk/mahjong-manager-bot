from DomainService import (
    match_service,
)
from repositories import match_repository
from DomainModel.entities.Match import Match
import pytest

dummy_matches1 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        tip_scores={}
    )
]


def test_ok_add_init(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=dummy_matches1,
    )
    mock_update = mocker.patch.object(
        match_repository,
        'update',
    )

    # Act
    result = match_service.add_or_drop_tip_score(
        'G0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu1',
        10,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.tip_scores) == 1
    assert result.tip_scores['U0123456789abcdefghijklmnopqrstu1'] == 10
    mock_update.assert_called_once()


dummy_matches2 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        tip_scores={'U0123456789abcdefghijklmnopqrstu2': 20}
    )
]


def test_ok_add_second(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=dummy_matches2,
    )
    mock_update = mocker.patch.object(
        match_repository,
        'update',
    )

    # Act
    result = match_service.add_or_drop_tip_score(
        'G0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu1',
        10,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.tip_scores) == 2
    assert result.tip_scores['U0123456789abcdefghijklmnopqrstu2'] == 20
    assert result.tip_scores['U0123456789abcdefghijklmnopqrstu1'] == 10
    mock_update.assert_called_once()


dummy_matches3 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        tip_scores={
            'U0123456789abcdefghijklmnopqrstu2': 20,
            'U0123456789abcdefghijklmnopqrstu1': 30,
        }
    )
]


def test_ok_update(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=dummy_matches3,
    )
    mock_update = mocker.patch.object(
        match_repository,
        'update',
    )

    # Act
    result = match_service.add_or_drop_tip_score(
        'G0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu1',
        10,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.tip_scores) == 2
    assert result.tip_scores['U0123456789abcdefghijklmnopqrstu2'] == 20
    assert result.tip_scores['U0123456789abcdefghijklmnopqrstu1'] == 10
    mock_update.assert_called_once()


dummy_matches3 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        tip_scores={
            'U0123456789abcdefghijklmnopqrstu2': 20,
            'U0123456789abcdefghijklmnopqrstu1': 30,
        }
    )
]


def test_ok_drop(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=dummy_matches3,
    )
    mock_update = mocker.patch.object(
        match_repository,
        'update',
    )

    # Act
    result = match_service.add_or_drop_tip_score(
        'G0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu1',
        None,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.tip_scores) == 1
    assert result.tip_scores['U0123456789abcdefghijklmnopqrstu2'] == 20
    mock_update.assert_called_once()


dummy_matches4 = [
    Match(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        tip_scores={
            'U0123456789abcdefghijklmnopqrstu1': 30,
        }
    )
]


def test_ok_drop_all(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=dummy_matches4,
    )
    mock_update = mocker.patch.object(
        match_repository,
        'update',
    )

    # Act
    result = match_service.add_or_drop_tip_score(
        999,
        'U0123456789abcdefghijklmnopqrstu1',
        None,
    )

    # Assert
    assert isinstance(result, Match)
    assert len(result.tip_scores) == 0
    mock_update.assert_called_once()


def test_ng_no_line_user_id(mocker):
    with pytest.raises(ValueError):
        # Arrange
        mock_find = mocker.patch.object(
            match_repository,
            'find',
        )
        mock_update = mocker.patch.object(
            match_repository,
            'update',
        )

        # Act
        match_service.add_or_drop_tip_score(
            'G0123456789abcdefghijklmnopqrstu1',
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
            'find',
            return_value=[],
        )
        mock_update = mocker.patch.object(
            match_repository,
            'update',
        )

        # Act
        match_service.add_or_drop_tip_score(
            'G0123456789abcdefghijklmnopqrstu1',
            'U0123456789abcdefghijklmnopqrstu1',
            10,
        )

        # Assert
        mock_update.assert_not_called()
