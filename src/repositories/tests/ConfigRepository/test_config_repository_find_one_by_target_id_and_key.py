from tests.dummies import generate_dummy_config_list
from repositories import session_scope, config_repository
from DomainModel.entities.Config import Config


def test_hit():
    # Arrange
    with session_scope() as session:
        dummy_config = generate_dummy_config_list()[0]
        config_repository.create(
            session=session,
            new_config=dummy_config,
        )

    # Act
    with session_scope() as session:
        result = config_repository.find_one_by_target_id_and_key(
            session=session,
            target_id=dummy_config.target_id,
            key=dummy_config.key,
        )

    # Assert
        assert isinstance(result, Config)
        assert result._id == dummy_config._id
        assert result.target_id == dummy_config.target_id
        assert result.key == dummy_config.key
        assert result.value == dummy_config.value


def test_not_hit():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[1:3]

        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )
    target_config = generate_dummy_config_list()[0]

    # Act
    with session_scope() as session:
        result = config_repository.find_one_by_target_id_and_key(
            session=session,
            target_id=target_config.target_id,
            key=target_config.key,
        )

    # Assert
        assert result is None
