from tests.dummies import generate_dummy_config, generate_dummy_config_list
from db_setting import Session
from repositories import session_scope
from repositories.config_repository import ConfigRepository
from domains.config import Config

session = Session()


def test_hit():
    # Arrange
    with session_scope() as session:
        dummyConfig = generate_dummy_config()
        ConfigRepository.create(
            session,
            dummyConfig,
        )

    # Act
    with session_scope() as session:
        result = ConfigRepository.find_one_by_target_id_and_key(
            session,
            dummyConfig.target_id,
            dummyConfig.key,
        )

    # Assert
        assert isinstance(result, Config)
        assert result.target_id == dummyConfig.target_id
        assert result.key == dummyConfig.key
        assert result.value == dummyConfig.value


def test_not_hit():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[1:3]

        for dummy_config in dummy_configs:
            ConfigRepository.create(
                session,
                dummy_config,
            )

    # Act
    with session_scope() as session:
        target_config = generate_dummy_config_list()[0]
        result = ConfigRepository.find_one_by_target_id_and_key(
            session,
            target_config.target_id,
            target_config.key,
        )

    # Assert
        assert result is None
