from tests.dummies import generate_dummy_config_list
from Repositories import session_scope, config_repository
from Domains.Entities.Config import Config


def test_success_find_records():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )

    # Act
    with session_scope() as session:
        result = config_repository.find_all(
            session=session,
        )

    # Assert
        assert len(result) == len(dummy_configs)
        for i in range(len(result)):
            assert isinstance(result[i], Config)
            assert result[i]._id == dummy_configs[i]._id
            assert result[i].target_id == dummy_configs[i].target_id
            assert result[i].key == dummy_configs[i].key
            assert result[i].value == dummy_configs[i].value


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    with session_scope() as session:
        result = config_repository.find_all(
            session=session,
        )

    # Assert
        assert len(result) == 0
