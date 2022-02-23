from typing import Tuple
import pytest
from domains.entities.Config import Config
from tests.dummies import generate_dummy_config_list
from repositories import session_scope, config_repository


@pytest.fixture(params=[
    ('U0123456789abcdefghijklmnopqrstu1', 'レート', '点1'),
    ('U0123456789abcdefghijklmnopqrstu1', 'レート', '点2'),
    ('U0123456789abcdefghijklmnopqrstu1', 'レート', '点3'),
    ('U0123456789abcdefghijklmnopqrstu1', 'レート', '点4'),
    ('U0123456789abcdefghijklmnopqrstu1', 'レート', '点5'),
    ('U0123456789abcdefghijklmnopqrstu1', 'レート', '点10'),
    ('U0123456789abcdefghijklmnopqrstu1', '順位点', ','.join(['20', '10', '-10', '-20'])),
    ('U0123456789abcdefghijklmnopqrstu1', '順位点', ','.join(['30', '10', '-10', '-30'])),
    ('U0123456789abcdefghijklmnopqrstu1', '飛び賞', '0'),
    ('U0123456789abcdefghijklmnopqrstu1', '飛び賞', '10'),
    ('U0123456789abcdefghijklmnopqrstu1', '飛び賞', '20'),
    ('U0123456789abcdefghijklmnopqrstu1', '飛び賞', '30'),
    ('U0123456789abcdefghijklmnopqrstu1', 'チップ', '0'),
    ('U0123456789abcdefghijklmnopqrstu1', 'チップ', '30'),
    ('U0123456789abcdefghijklmnopqrstu1', '人数', '3'),
    ('U0123456789abcdefghijklmnopqrstu1', '人数', '4'),
    ('U0123456789abcdefghijklmnopqrstu1', '端数計算方法', '3万点以下切り上げ/以上切り捨て'),
    ('U0123456789abcdefghijklmnopqrstu1', '端数計算方法', '五捨六入'),
    ('U0123456789abcdefghijklmnopqrstu1', '端数計算方法', '四捨五入'),
    ('U0123456789abcdefghijklmnopqrstu1', '端数計算方法', '切り捨て'),
    ('U0123456789abcdefghijklmnopqrstu1', '端数計算方法', '切り上げ'),
])
def case1(request) -> Tuple[str, str, str]:
    return request.param


def test_success(case1):
    # Arrange

    # Act
    Config(
        target_id=case1[0],
        key=case1[1],
        value=case1[2],
        _id=1,
    )

    # Assert


@pytest.fixture(params=[
    ('U0123456789abcdefghijklmnopqrstu1', 'dummy', '10'),
])
def case2(request) -> Tuple[str, str, str]:
    return request.param


def test_fail_with_invalid_key(case2):
    with pytest.raises(ValueError):
        # Arrange

        # Act
        Config(
            target_id=case2[0],
            key=case2[1],
            value=case2[2],
            _id=1,
        )

        # Assert


@pytest.fixture(params=[
    ('U0123456789abcdefghijklmnopqrstu1', 'レート', '10'),
])
def case3(request) -> Tuple[str, str, str]:
    return request.param


def test_fail_with_invalid_value(case3):
    with pytest.raises(ValueError):
        # Arrange

        # Act
        Config(
            target_id=case3[0],
            key=case3[1],
            value=case3[2],
            _id=1,
        )

        # Assert
