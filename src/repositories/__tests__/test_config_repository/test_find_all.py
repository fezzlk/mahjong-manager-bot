from tests.dummies import generate_dummy_config_list
from db_setting import Session
from repositories import session_scope
from repositories.config_repository import ConfigRepository
from domains.config import Config

session = Session()


def test_success_find_records():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()
        for dummyConfig in dummy_configs:
            ConfigRepository.create(
                session,
                dummyConfig,
            )

    # Act
    with session_scope() as session:
        result = ConfigRepository.find_all(
            session,
        )

    # Assert
        assert len(result) == len(dummy_configs)
        for i in range(len(result)):
            assert isinstance(result[i], Config)
            assert result[i].target_id == dummy_configs[i].target_id
            assert result[i].key == dummy_configs[i].key
            assert result[i].value == dummy_configs[i].value


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    with session_scope() as session:
        result = ConfigRepository.find_all(
            session,
        )

    # Assert
        assert len(result) == 0
