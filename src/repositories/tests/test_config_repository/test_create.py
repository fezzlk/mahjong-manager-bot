from tests.dummies import generate_dummy_config
from db_setting import Session
from repositories import session_scope
from repositories.config_repository import ConfigRepository

session = Session()


def test_success():
    # Arrange
    with session_scope() as session:
        dummyConfig = generate_dummy_config()

    # Act
        ConfigRepository.create(
            session,
            dummyConfig,
        )

    # Assert
    # Do nothing
