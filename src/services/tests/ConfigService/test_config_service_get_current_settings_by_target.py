from tests.dummies import (
    generate_dummy_config_list,
)
from services import (
    config_service,
)
from DomainModel.entities.Config import DEFAULT_CONFIGS
from repositories import session_scope, config_repository


def test_success():
    # Arrage
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:6]
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )
    expected_settings = {
        'レート': '点2',
        '順位点': ','.join(['20', '10', '-10', '-20']),
        '飛び賞': '30',
        'チップ': 'なし',
        '人数': '4',
        '端数計算方法': '3万点以下切り上げ/以上切り捨て',
    }

    # Act
    result = config_service.get_current_settings_by_target(
        target_id=dummy_configs[0].target_id,
    )

    # Assert
    assert len(result) == len(expected_settings)
    for key, value in result.items():
        assert expected_settings[key] == value


def test_success_get_default_settings():
    # Arrage
    dummy_config = generate_dummy_config_list()[0]

    # Act
    result = config_service.get_current_settings_by_target(
        target_id=dummy_config.target_id,
    )

    # Assert
    assert len(result) == len(DEFAULT_CONFIGS)
    for key, value in result.items():
        assert DEFAULT_CONFIGS[key] == value
