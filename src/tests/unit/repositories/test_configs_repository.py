from tests.mocks import MockConfig
from db_setting import Base, Engine, Session
from repositories import session_scope
from repositories.configs import ConfigsRepository

session = Session()
Base.metadata.create_all(bind=Engine)


def test_configs_repository_create():
    mockConfig = MockConfig()

    with session_scope() as session:
        ConfigsRepository.create(
            session,
            target_id=mockConfig.target_id,
            key=mockConfig.key,
            value=mockConfig.value,
        )
