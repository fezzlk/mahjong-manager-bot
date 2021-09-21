from tests.dummies import generate_dummy_config
from db_setting import Session
from repositories import session_scope
from repositories.ConfigRepository import ConfigRepository

session = Session()


def test_success():
    # Arrange
    dummy_config = generate_dummy_config()

    # Act
    with session_scope() as session:
        ConfigRepository.create(
            session,
            dummy_config,
        )

    # Assert
    with session_scope() as session:
        result = ConfigRepository.find_all(
            session,
        )
        assert len(result) == 1
        assert result[0].target_id == dummy_config.target_id
        assert result[0].key == dummy_config.key
        assert result[0].value == dummy_config.value
