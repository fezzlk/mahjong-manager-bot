import pytest
from typing import Tuple
from tests.dummies import (
    generate_dummy_config_list,
)
from DomainService import (
    config_service,
)
from repositories import session_scope, group_setting_repository


@pytest.fixture(params=[
    ('レート', '点3'),
    ('順位点', ','.join(['20', '10', '-10', '-20'])),
    ('飛び賞', '10'),
    ('チップ', '0'),
    ('人数', '4'),
    ('端数計算方法', '3万点以下切り上げ/以上切り捨て'),
])
def case(request) -> Tuple[str, str]:
    return request.param


def test_success_get_default_config(case):
    # Arrage
    dummy_config = generate_dummy_config_list()[0]

    # Act
    result = config_service.get_value_by_key(
        target_id=dummy_config.target_id,
        key=case[0],
    )

    # Assert
    assert result == case[1]


def test_success_get_updated_config():
    # Arrage
    with session_scope() as session:
        dummy_configs = generate_dummy_config_list()[:6]
        for dummy_config in dummy_configs:
            group_setting_repository.create(
                session=session,
                new_config=dummy_config,
            )

    # Act
    result = config_service.get_value_by_key(
        target_id=dummy_configs[0].target_id,
        key=dummy_configs[0].key,
    )

    # Assert
    assert result == dummy_configs[0].value
