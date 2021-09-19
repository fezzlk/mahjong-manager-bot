from tests.mocks import generateMockConfig
from db_setting import Base, Engine, Session
from repositories import session_scope
from repositories.config_repository import ConfigRepository
from domains.config import Config

session = Session()
Base.metadata.create_all(bind=Engine)


def test_config_repository_create():
    with session_scope() as session:
        # Arrange
        mockConfig = generateMockConfig()

        # Act
        ConfigRepository.create(
            session,
            mockConfig,
        )

        # Assert


def test_configs_repository_find_one_by_target_id_and_key():
    with session_scope() as session:
        # Arrange
        mockConfig = generateMockConfig()
        ConfigRepository.create(
            session,
            mockConfig,
        )

        # Act
        result = ConfigRepository.find_one_by_target_id_and_key(
            session,
            mockConfig.target_id,
            mockConfig.key,
        )

        # Assert
        assert isinstance(result, Config)
        assert result.target_id == mockConfig.target_id
        assert result.key == mockConfig.key
        assert result.value == mockConfig.value
