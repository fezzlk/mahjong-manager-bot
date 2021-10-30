from tests.dummies import (
    generate_dummy_config_list,
)
from services import (
    config_service,
)
from repositories import session_scope, config_repository
from domains.Config import Config


def test_success_get_all():
    # Arrage
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:6]
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )

    # Act
    result = config_service.get()

    # Assert
    assert len(result) == len(dummy_configs)
    for i in range(len(result)):
        assert isinstance(result[i], Config)
        assert result[i]._id == dummy_configs[i]._id
        assert result[i].target_id == dummy_configs[i].target_id
        assert result[i].key == dummy_configs[i].key
        assert result[i].value == dummy_configs[i].value


def test_success_get_some_records():
    # Arrage
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:6]
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )
        target_configs = generate_dummy_config_list()[:3]

    # Act
    result = config_service.get([1, 2, 3])

    # Assert
    assert len(result) == len(target_configs)
    for i in range(len(result)):
        assert isinstance(result[i], Config)
        assert result[i]._id == target_configs[i]._id
        assert result[i].target_id == target_configs[i].target_id
        assert result[i].key == target_configs[i].key
        assert result[i].value == target_configs[i].value


def test_success_get_0_record():
    # Arrage
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:6]
        for dummy_config in dummy_configs:
            config_repository.create(
                session=session,
                new_config=dummy_config,
            )

    # Act
    result = config_service.get([7])

    # Assert
    assert len(result) == 0
