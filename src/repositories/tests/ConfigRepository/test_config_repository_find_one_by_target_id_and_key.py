import pytest
from tests.dummies import generate_dummy_config, generate_dummy_config_list
from db_setting import Session
from repositories import session_scope, config_repository
from domains.Config import Config

session = Session()


def test_hit():
    # Arrange
    with session_scope() as session:
        dummy_config = generate_dummy_config()
        config_repository.create(
            session,
            dummy_config,
        )

    # Act
    with session_scope() as session:
        result = config_repository.find_one_by_target_id_and_key(
            session,
            dummy_config.target_id,
            dummy_config.key,
        )

    # Assert
        assert isinstance(result, Config)
        assert result.target_id == dummy_config.target_id
        assert result.key == dummy_config.key
        assert result.value == dummy_config.value


def test_not_hit():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[1:3]

        for dummy_config in dummy_configs:
            config_repository.create(
                session,
                dummy_config,
            )
    target_config = generate_dummy_config_list()[0]

    # Act
    with session_scope() as session:
        result = config_repository.find_one_by_target_id_and_key(
            session,
            target_config.target_id,
            target_config.key,
        )

    # Assert
        assert result is None


def test_NG_with_target_id_none():
    with pytest.raises(ValueError):
        # Arrange
        target_config = generate_dummy_config_list()[0]

        # Act
        with session_scope() as session:
            config_repository.find_one_by_target_id_and_key(
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
            config_repository.find_one_by_target_id_and_key(
                session,
                target_config.target_id,
                None,
            )

        # Assert
        # Do nothing
