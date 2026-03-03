from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_service import group_setting_service
from repositories import group_repository

dummy_line_group_id = "G0123456789abcdefghijklmnopqrstu1"

dummy_group_with_settings = Group(
    line_group_id=dummy_line_group_id,
    mode=GroupMode.wait.value,
    settings=EmbeddedGroupSettings(
        rate=0,
        ranking_prize=[20, 10, -10, -20],
        chip_rate=0,
        tobi_prize=10,
        num_of_players=4,
        rounding_method=0,
    ),
)

dummy_group_without_settings = Group(
    line_group_id=dummy_line_group_id,
    mode=GroupMode.wait.value,
    settings=None,
)


def test_ok_hit_group_setting(mocker):
    # group.settings が設定済みの場合、settings がそのまま返り update は呼ばれないこと
    mocker.patch.object(
        group_repository,
        "find",
        return_value=[dummy_group_with_settings],
    )
    mock_update_settings = mocker.patch.object(
        group_repository,
        "update_settings",
    )

    result = group_setting_service.find_or_create(dummy_line_group_id)

    assert isinstance(result, EmbeddedGroupSettings)
    assert result.rate == 0
    mock_update_settings.assert_not_called()


def test_ok_no_group_setting(mocker):
    # group は存在するが settings が None の場合、デフォルト設定が保存されて返ること
    mocker.patch.object(
        group_repository,
        "find",
        return_value=[dummy_group_without_settings],
    )
    mock_update_settings = mocker.patch.object(
        group_repository,
        "update_settings",
    )

    result = group_setting_service.find_or_create(dummy_line_group_id)

    assert isinstance(result, EmbeddedGroupSettings)
    mock_update_settings.assert_called_once()
