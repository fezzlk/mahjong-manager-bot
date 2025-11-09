from DomainModel.entities.GroupSetting import GroupSetting
from DomainService import (
    group_setting_service,
)
from repositories import group_setting_repository

dummy_group_settings = [
    GroupSetting(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        rate=0,
        ranking_prize=[20, 10, -10, -20],
        chip_rate=0,
        tobi_prize=10,
        num_of_players=4,
        rounding_method=0,
    ),
]


def test_ok_hit_group_setting(mocker):
    # Arrange
    mocker.patch.object(
        group_setting_repository,
        "find",
        return_value=dummy_group_settings,
    )
    mock_create = mocker.patch.object(
        group_setting_repository,
        "create",
        return_value=dummy_group_settings[0],
    )

    # Act
    result = group_setting_service.find_or_create("G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert isinstance(result, GroupSetting)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    mock_create.assert_not_called()


def test_ok_no_group_setting(mocker):
    # Arrange
    mocker.patch.object(
        group_setting_repository,
        "find",
        return_value=[],
    )

    mock_create = mocker.patch.object(
        group_setting_repository,
        "create",
        return_value=dummy_group_settings[0],
    )

    # Act
    result = group_setting_service.find_or_create("G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert isinstance(result, GroupSetting)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    mock_create.assert_called_once()
