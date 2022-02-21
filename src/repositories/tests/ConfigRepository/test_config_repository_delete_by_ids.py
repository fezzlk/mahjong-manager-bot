from tests.dummies import generate_dummy_config_list
from repositories import session_scope, config_repository
from entities.Config import Config


def test_hit_with_ids():
    # Arrange
    dummy_configs = generate_dummy_config_list()[:3]
    with session_scope() as session:
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )
    other_configs = dummy_configs[:1]
    target_configs = dummy_configs[1:3]
    ids = [target_config._id for target_config in target_configs]

    # Act
    with session_scope() as session:
        result = config_repository.delete_by_ids(
            session=session,
            ids=ids,
        )

    # Assert
    assert result == len(target_configs)
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


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:3]
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )
    target_configs = generate_dummy_config_list()[3:6]
    ids = [target_config._id for target_config in target_configs]

    # Act
    with session_scope() as session:
        result = config_repository.delete_by_ids(
            session=session,
            ids=ids,
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
