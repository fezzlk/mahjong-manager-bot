from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.match import Match
from domain_service import (
    match_service,
)
from repositories import match_repository

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    ),
]


def test_ok_no_group(mocker):
    # Arrange
    mock_create = mocker.patch.object(
        match_repository,
        "create",
        return_value=dummy_matches[0],
    )

    # Act
    result = match_service.create_with_line_group_id("G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert isinstance(result, Match)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    mock_create.assert_called_once()


def test_assigns_default_name_and_copies_settings(mocker):
    # Arrange
    mocker.patch.object(match_repository, "create")
    mocker.patch.object(match_repository, "find", return_value=[])
    settings = EmbeddedGroupSettings(rate=3)

    # Act
    result = match_service.create_with_line_group_id(
        "G0123456789abcdefghijklmnopqrstu1",
        settings=settings,
    )

    # Assert
    assert result.settings == settings
    assert result.name is not None
    assert "/" in result.name  # "M/D" 形式


def test_appends_sequence_suffix_when_same_day_match_exists(mocker):
    # Arrange
    mocker.patch.object(match_repository, "create")
    mocker.patch.object(
        match_repository,
        "find",
        return_value=[dummy_matches[0]],  # 当日既に1件作成済みという想定
    )

    # Act
    result = match_service.create_with_line_group_id("G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert result.name.endswith("(2)")
