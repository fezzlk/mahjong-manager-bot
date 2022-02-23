import pytest
from domains.entities.Config import Config
from tests.dummies import generate_dummy_config_list
from repositories import session_scope, config_repository


def test_success():
    # Arrange
    dummy_config = generate_dummy_config_list()[0]

    # Act
    with session_scope() as session:
        result = config_repository.create(
            session=session,
            new_config=dummy_config,
        )

    # Assert
    assert isinstance(result, Config)
    assert result._id == dummy_config._id
    assert result.target_id == dummy_config.target_id
    assert result.key == dummy_config.key
    assert result.value == dummy_config.value

    with session_scope() as session:
        record_on_db = config_repository.find_all(
            session,
        )
        assert len(record_on_db) == 1
        assert record_on_db[0]._id == dummy_config._id
        assert record_on_db[0].target_id == dummy_config.target_id
        assert record_on_db[0].key == dummy_config.key
        assert record_on_db[0].value == dummy_config.value
