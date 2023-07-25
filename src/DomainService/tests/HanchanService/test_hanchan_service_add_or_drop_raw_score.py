from DomainService import (
    hanchan_service,
)
from repositories import hanchan_repository
from DomainModel.entities.Hanchan import Hanchan
import pytest

dummy_hanchans1 = [
    Hanchan(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        match_id=1,
        raw_scores={}
    )
]


def test_ok_add_init(mocker):
    # Arrange
    mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=dummy_hanchans1,
    )
    mock_update = mocker.patch.object(
        hanchan_repository,
        'update',
    )

    # Act
    result = hanchan_service.add_or_drop_raw_score(
        'G0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu1',
        1000,
    )

    # Assert
    assert isinstance(result, Hanchan)
    assert len(result.raw_scores) == 1
    assert result.raw_scores['U0123456789abcdefghijklmnopqrstu1'] == 1000
    mock_update.assert_called_once_with(
        {'_id': 999},
        {'raw_scores': {'U0123456789abcdefghijklmnopqrstu1': 1000}},
    )


dummy_hanchans2 = [
    Hanchan(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        match_id=1,
        raw_scores={'U0123456789abcdefghijklmnopqrstu2': 2000}
    )
]


def test_ok_add_second(mocker):
    # Arrange
    mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=dummy_hanchans2,
    )
    mock_update = mocker.patch.object(
        hanchan_repository,
        'update',
    )

    # Act
    result = hanchan_service.add_or_drop_raw_score(
        'G0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu1',
        1000,
    )

    # Assert
    assert isinstance(result, Hanchan)
    assert len(result.raw_scores) == 2
    assert result.raw_scores['U0123456789abcdefghijklmnopqrstu2'] == 2000
    assert result.raw_scores['U0123456789abcdefghijklmnopqrstu1'] == 1000
    mock_update.assert_called_once_with(
        {'_id': 999},
        {'raw_scores': {
            'U0123456789abcdefghijklmnopqrstu2': 2000,
            'U0123456789abcdefghijklmnopqrstu1': 1000,
        }},
    )


dummy_hanchans3 = [
    Hanchan(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        match_id=1,
        raw_scores={
            'U0123456789abcdefghijklmnopqrstu2': 2000,
            'U0123456789abcdefghijklmnopqrstu1': 3000,
        }
    )
]


def test_ok_update(mocker):
    # Arrange
    mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=dummy_hanchans3,
    )
    mock_update = mocker.patch.object(
        hanchan_repository,
        'update',
    )

    # Act
    result = hanchan_service.add_or_drop_raw_score(
        'G0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu1',
        1000,
    )

    # Assert
    assert isinstance(result, Hanchan)
    assert len(result.raw_scores) == 2
    assert result.raw_scores['U0123456789abcdefghijklmnopqrstu2'] == 2000
    assert result.raw_scores['U0123456789abcdefghijklmnopqrstu1'] == 1000
    mock_update.assert_called_once_with(
        {'_id': 999},
        {'raw_scores': {
            'U0123456789abcdefghijklmnopqrstu2': 2000,
            'U0123456789abcdefghijklmnopqrstu1': 1000,
        }},
    )


dummy_hanchans3 = [
    Hanchan(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        match_id=1,
        raw_scores={
            'U0123456789abcdefghijklmnopqrstu2': 2000,
            'U0123456789abcdefghijklmnopqrstu1': 3000,
        }
    )
]


def test_ok_drop(mocker):
    # Arrange
    mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=dummy_hanchans3,
    )
    mock_update = mocker.patch.object(
        hanchan_repository,
        'update',
    )

    # Act
    result = hanchan_service.add_or_drop_raw_score(
        'G0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu1',
        None,
    )

    # Assert
    assert isinstance(result, Hanchan)
    assert len(result.raw_scores) == 1
    assert result.raw_scores['U0123456789abcdefghijklmnopqrstu2'] == 2000
    mock_update.assert_called_once_with(
        {'_id': 999},
        {'raw_scores': {
            'U0123456789abcdefghijklmnopqrstu2': 2000,
        }},
    )


dummy_hanchans4 = [
    Hanchan(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        match_id=1,
        raw_scores={
            'U0123456789abcdefghijklmnopqrstu1': 3000,
        }
    )
]


def test_ok_drop_all(mocker):
    # Arrange
    mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=dummy_hanchans4,
    )
    mock_update = mocker.patch.object(
        hanchan_repository,
        'update',
    )

    # Act
    result = hanchan_service.add_or_drop_raw_score(
        'G0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu1',
        None,
    )

    # Assert
    assert isinstance(result, Hanchan)
    assert len(result.raw_scores) == 0
    mock_update.assert_called_once_with(
        {'_id': 999},
        {'raw_scores': {}},
    )


def test_ng_no_line_user_id(mocker):
    with pytest.raises(ValueError):
        # Arrange
        mock_find = mocker.patch.object(
            hanchan_repository,
            'find',
        )
        mock_update = mocker.patch.object(
            hanchan_repository,
            'update',
        )

        # Act
        hanchan_service.add_or_drop_raw_score(
            'G0123456789abcdefghijklmnopqrstu1',
            None,
            1000,
        )

        # Assert
        mock_find.assert_not_called()
        mock_update.assert_not_called()


def test_ng_no_hanchan(mocker):
    with pytest.raises(ValueError):
        # Arrange
        mocker.patch.object(
            hanchan_repository,
            'find',
            return_value=[],
        )
        mock_update = mocker.patch.object(
            hanchan_repository,
            'update',
        )

        # Act
        hanchan_service.add_or_drop_raw_score(
            'G0123456789abcdefghijklmnopqrstu1',
            'U0123456789abcdefghijklmnopqrstu1',
            1000,
        )

        # Assert
        mock_update.assert_not_called()
