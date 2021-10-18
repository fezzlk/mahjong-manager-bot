from tests.dummies import generate_dummy_config_list
from repositories import session_scope, config_repository
from domains.Config import Config


def test_hit_records():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:6]
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )
    target_configs = generate_dummy_config_list()[:2]
    target_id = target_configs[0].target_id

    # Act
    with session_scope() as session:
        result = config_repository.find_by_target_id(
            session=session,
            target_id=target_id,
        )

    # Assert
        assert len(result) == len(target_configs)
        for i in range(len(result)):
            assert isinstance(result[i], Config)
            assert result[i].target_id == dummy_configs[i].target_id
            assert result[i].key == dummy_configs[i].key
            assert result[i].value == dummy_configs[i].value


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:5]
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )
    target_id = generate_dummy_config_list()[5].target_id

    # Act
    with session_scope() as session:
        result = config_repository.find_by_target_id(
            session=session,
            target_id=target_id,
        )

    # Assert
        assert len(result) == 0
