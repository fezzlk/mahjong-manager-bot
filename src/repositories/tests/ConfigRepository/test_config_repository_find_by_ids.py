from tests.dummies import generate_dummy_config_list
from db_setting import Session
from repositories import session_scope, config_repository
from domains.Config import Config

session = Session()


def test_hit_with_ids():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:3]
        for dummy_config in dummy_configs:
            config_repository.create(
                session,
                dummy_config,
            )
    target_configs = generate_dummy_config_list()[1:3]
    ids = [target_config._id for target_config in target_configs]

    # Act
    with session_scope() as session:
        result = config_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == len(target_configs)
        for i in range(len(result)):
            assert isinstance(result[i], Config)
            assert result[i].target_id == target_configs[i].target_id
            assert result[i].key == target_configs[i].key
            assert result[i].value == target_configs[i].value


def test_hit_with_an_id_as_not_list():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:3]
        for dummy_config in dummy_configs:
            config_repository.create(
                session,
                dummy_config,
            )
    target_config = generate_dummy_config_list()[2]
    target_config_id = target_config._id

    # Act
    with session_scope() as session:
        result = config_repository.find_by_ids(
            session,
            target_config_id,
        )

    # Assert
        assert len(result) == 1
        assert result[0].target_id == target_config.target_id
        assert result[0].key == target_config.key
        assert result[0].value == target_config.value


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:3]
        for dummy_config in dummy_configs:
            config_repository.create(
                session,
                dummy_config,
            )
    target_configs = generate_dummy_config_list()[3:6]
    ids = [target_config._id for target_config in target_configs]

    # Act
    with session_scope() as session:
        result = config_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == 0
