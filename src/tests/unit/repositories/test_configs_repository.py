from tests.mocks import MockConfig
from db_setting import Base, Engine, Session
from repositories import session_scope
from repositories.configs import ConfigsRepository
from models import Configs

session = Session()
Base.metadata.create_all(bind=Engine)


def test_configs_repository_create():
    # Arrange
    mockConfig = MockConfig()

    with session_scope() as session:
        # Act
        ConfigsRepository.create(
            session,
            target_id=mockConfig.target_id,
            key=mockConfig.key,
            value=mockConfig.value,
        )

        # Assert


def test_configs_repository_find():
    # Arrange
    mockConfig = MockConfig()

    with session_scope() as session:
        # Act
        result = ConfigsRepository.find(
            session,
            target_id=mockConfig.target_id,
            key=mockConfig.key,
        )

        # Assert
        assert isinstance(result, Configs)
        assert result.target_id == mockConfig.target_id
        assert result.key == mockConfig.key
        assert result.value == mockConfig.value
