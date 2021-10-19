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
        config_repository.delete_by_target_id_and_key(
            session=session,
            target_id=target_config.target_id,
            key=target_config.key,
        )

    # Assert
    with session_scope() as session:
        result = config_repository.find_all(
            session=session,
        )
        assert len(result) == len(other_configs)
        for i in range(len(result)):
            assert isinstance(result[i], Config)
            assert result[i].target_id == other_configs[i].target_id
            assert result[i].key == other_configs[i].key
            assert result[i].value == other_configs[i].value
