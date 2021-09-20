from tests.dummies import generate_dummy_config_list
from db_setting import Session
from repositories import session_scope
from repositories.config_repository import ConfigRepository
from domains.config import Config

session = Session()


def test_hit_with_ids():
    # Arrange
    dummy_configs = generate_dummy_config_list()[:3]
    with session_scope() as session:
        for dummy_config in dummy_configs:
            ConfigRepository.create(
                session,
                dummy_config,
            )
    other_configs = dummy_configs[:1]
    target_configs = dummy_configs[1:3]
    ids = [target_config._id for target_config in target_configs]

    # Act
    with session_scope() as session:
        ConfigRepository.delete_by_ids(
            session,
            ids,
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


def test_hit_with_an_id_as_not_list():
    # Arrange
    dummy_configs = generate_dummy_config_list()[:3]
    with session_scope() as session:
        for dummy_config in dummy_configs:
            ConfigRepository.create(
                session,
                dummy_config,
            )
    other_configs = dummy_configs[:2]
    target_config = dummy_configs[2]
    target_config_id = target_config._id

    # Act
    with session_scope() as session:
        result = ConfigRepository.delete_by_ids(
            session,
            target_config_id,
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


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:3]
        for dummy_config in dummy_configs:
            ConfigRepository.create(
                session,
                dummy_config,
            )
    target_configs = generate_dummy_config_list()[3:6]
    ids = [target_config._id for target_config in target_configs]

    # Act
    with session_scope() as session:
        result = ConfigRepository.delete_by_ids(
            session,
            ids,
        )

    # Assert
    with session_scope() as session:
        result = ConfigRepository.find_all(
            session,
        )
        assert len(result) == len(dummy_configs)
        for i in range(len(result)):
            assert isinstance(result[i], Config)
            assert result[i].target_id == dummy_configs[i].target_id
            assert result[i].key == dummy_configs[i].key
            assert result[i].value == dummy_configs[i].value
