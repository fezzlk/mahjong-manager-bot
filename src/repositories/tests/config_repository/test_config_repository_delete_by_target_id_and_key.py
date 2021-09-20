
import pytest
from tests.dummies import generate_dummy_config_list
from db_setting import Session
from repositories import session_scope
from repositories.config_repository import ConfigRepository
from domains.config import Config

session = Session()


def test_success():
    # Arrange
    dummy_configs = generate_dummy_config_list()[:6]
    with session_scope() as session:
        for dummy_config in dummy_configs:
            ConfigRepository.create(
                session,
                dummy_config,
            )
    other_configs = dummy_configs[:5]
    target_config = dummy_configs[5]

    # Act
    with session_scope() as session:
        ConfigRepository.delete_by_target_id_and_key(
            session,
            target_config.target_id,
            target_config.key,
        )

    # Assert
    with session_scope() as session:
        result = ConfigRepository.find_all(
            session,
        )
        assert len(result) == len(other_configs)
        for i in range(len(result)):
            assert isinstance(result[i], Config)
            assert result[i].target_id == other_configs[i].target_id
            assert result[i].key == other_configs[i].key
            assert result[i].value == other_configs[i].value


def test_NG_with_target_id_none():
    with pytest.raises(ValueError):
        # Arrange
        target_config = generate_dummy_config_list()[0]

        # Act
        with session_scope() as session:
            ConfigRepository.find_one_by_target_id_and_key(
                session,
                None,
                target_config.key,
            )

        # Assert
        # Do nothing


def test_NG_with_key_none():
    with pytest.raises(ValueError):
        # Arrange
        target_config = generate_dummy_config_list()[0]

        # Act
        with session_scope() as session:
            ConfigRepository.find_one_by_target_id_and_key(
                session,
                target_config.target_id,
                None,
            )

        # Assert
        # Do nothing
