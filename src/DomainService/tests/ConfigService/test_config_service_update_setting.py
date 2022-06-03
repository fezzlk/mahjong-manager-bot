from tests.dummies import (
    generate_dummy_config_list,
)
from DomainService import (
    config_service,
)
from DomainModel.entities.Config import DEFAULT_CONFIGS
from repositories import session_scope, config_repository


def test_success_to_original_from_default():
    # Arrange
    dummy_config = generate_dummy_config_list()[0]
    expected_settings = {
        'レート': '点3',
        '順位点': ','.join(['20', '10', '-10', '-20']),
        '飛び賞': '30',
        'チップ': 'なし',
        '人数': '4',
        '端数計算方法': '3万点以下切り上げ/以上切り捨て',
    }

    # Act
    config_service.update_setting(
        target_id=dummy_config.target_id,
        key=dummy_config.key,
        value=dummy_config.value,
    )

    # Assert
    result = config_service.get_current_settings_by_target(
        target_id=dummy_config.target_id,
    )
    assert len(result) == len(expected_settings)
    for key, value in result.items():
        assert expected_settings[key] == value
    with session_scope() as session:
        record_on_db = config_repository.find_all(session)
        assert len(record_on_db) == 1


def test_success_to_original_from_original():
    # Arrange
    dummy_config = generate_dummy_config_list()[3]
    with session_scope() as session:
        config_repository.create(
            session=session,
            new_config=dummy_config,
        )
    after_value = '30'
    expected_settings = {
        'レート': '点3',
        '順位点': ','.join(['20', '10', '-10', '-20']),
        '飛び賞': '30',
        'チップ': 'なし',
        '人数': '4',
        '端数計算方法': '3万点以下切り上げ/以上切り捨て',
    }

    # Act
    config_service.update_setting(
        target_id=dummy_config.target_id,
        key=dummy_config.key,
        value=after_value,
    )

    # Assert
    result = config_service.get_current_settings_by_target(
        target_id=dummy_config.target_id,
    )
    assert len(result) == len(expected_settings)
    for key, value in result.items():
        assert expected_settings[key] == value
    with session_scope() as session:
        record_on_db = config_repository.find_all(session)
        assert len(record_on_db) == 1


def test_success_to_default_from_original():
    # Arrange
    dummy_config = generate_dummy_config_list()[3]
    with session_scope() as session:
        config_repository.create(
            session=session,
            new_config=dummy_config,
        )

    # Act
    config_service.update_setting(
        target_id=dummy_config.target_id,
        key=dummy_config.key,
        value=DEFAULT_CONFIGS[dummy_config.key],
    )

    # Assert
    result = config_service.get_current_settings_by_target(
        target_id=dummy_config.target_id,
    )
    assert len(result) == len(DEFAULT_CONFIGS)
    for key, value in result.items():
        assert DEFAULT_CONFIGS[key] == value
    with session_scope() as session:
        record_on_db = config_repository.find_all(session)
        assert len(record_on_db) == 0


def test_success_to_default_from_default():
    # Arrange
    dummy_config = generate_dummy_config_list()[3]

    # Act
    config_service.update_setting(
        target_id=dummy_config.target_id,
        key=dummy_config.key,
        value=DEFAULT_CONFIGS[dummy_config.key],
    )

    # Assert
    result = config_service.get_current_settings_by_target(
        target_id=dummy_config.target_id,
    )
    assert len(result) == len(DEFAULT_CONFIGS)
    for key, value in result.items():
        assert DEFAULT_CONFIGS[key] == value
    with session_scope() as session:
        record_on_db = config_repository.find_all(session)
        assert len(record_on_db) == 0
