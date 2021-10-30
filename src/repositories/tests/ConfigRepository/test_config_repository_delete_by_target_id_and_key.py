from tests.dummies import generate_dummy_config_list
from repositories import session_scope, config_repository
from domains.Config import Config


def test_success():
    # Arrange
    dummy_configs = generate_dummy_config_list()[:6]
    with session_scope() as session:
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )
    other_configs = dummy_configs[:5]
    target_config = dummy_configs[5]

    # Act
    with session_scope() as session:
        result = config_repository.delete_by_target_id_and_key(
            session=session,
            target_id=target_config.target_id,
            key=target_config.key,
        )

    # Assert
    assert result == 1
    with session_scope() as session:
        record_on_db = config_repository.find_all(
            session=session,
        )
        assert len(record_on_db) == len(other_configs)
        for i in range(len(record_on_db)):
            assert isinstance(record_on_db[i], Config)
            assert record_on_db[i]._id == other_configs[i]._id
            assert record_on_db[i].target_id == other_configs[i].target_id
            assert record_on_db[i].key == other_configs[i].key
            assert record_on_db[i].value == other_configs[i].value


def test_target_id_mismatch():
    # Arrange
    dummy_configs = generate_dummy_config_list()[:6]
    with session_scope() as session:
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )

    # Act
    with session_scope() as session:
        result = config_repository.delete_by_target_id_and_key(
            session=session,
            target_id=dummy_configs[2].target_id,
            key=dummy_configs[1].key,
        )

    # Assert
    assert result == 0
    with session_scope() as session:
        record_on_db = config_repository.find_all(
            session=session,
        )
        assert len(record_on_db) == len(dummy_configs)
        for i in range(len(record_on_db)):
            assert isinstance(record_on_db[i], Config)
            assert record_on_db[i]._id == dummy_configs[i]._id
            assert record_on_db[i].target_id == dummy_configs[i].target_id
            assert record_on_db[i].key == dummy_configs[i].key
            assert record_on_db[i].value == dummy_configs[i].value


def test_key_mismatch():
    # Arrange
    dummy_configs = generate_dummy_config_list()[:6]
    with session_scope() as session:
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )
    other_configs = dummy_configs[:5]
    target_config = dummy_configs[5]

    # Act
    with session_scope() as session:
        result = config_repository.delete_by_target_id_and_key(
            session=session,
            target_id=target_config.target_id,
            key=other_configs[4].key,
        )

    # Assert
    assert result == 0
    with session_scope() as session:
        record_on_db = config_repository.find_all(
            session=session,
        )
        assert len(record_on_db) == len(dummy_configs)
        for i in range(len(record_on_db)):
            assert isinstance(record_on_db[i], Config)
            assert record_on_db[i]._id == dummy_configs[i]._id
            assert record_on_db[i].target_id == dummy_configs[i].target_id
            assert record_on_db[i].key == dummy_configs[i].key
            assert record_on_db[i].value == dummy_configs[i].value
