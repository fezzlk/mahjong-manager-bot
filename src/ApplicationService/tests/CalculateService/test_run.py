from ApplicationService import (
    calculate_service,
)
from typing import Dict
import pytest


@pytest.fixture(params=[
    (
        {
            'line_user_id1': 10000,
            'line_user_id2': 20000,
            'line_user_id3': 30000,
            'line_user_id4': 40000,
        },
        [20, 10, -10, -20],
    ),
    (
        {
            'line_user_id1': 19999,
            'line_user_id2': 20000,
            'line_user_id3': 30000,
            'line_user_id4': 40000,
        },
        [30, 10, -10, -30],
    ),
    (
        {
            'line_user_id1': 10000,
            'line_user_id2': 20000,
            'line_user_id3': 30000,
            'line_user_id4': 40000,
        },
        [20, -10, 10, -20],
    ),
    (
        {
            'line_user_id3': 30000,
            'line_user_id2': 20000,
            'line_user_id1': 10000,
            'line_user_id4': 40000,
        },
        [20, -10, 10, -20],
    ),
])
def text_case1(request):
    return request.param


def test_ok(text_case1):
    # Arrange

    # Act
    result = calculate_service.run(
        points=text_case1[0],
        ranking_prize=text_case1[1],
        tobi_prize=10,
        rounding_method='五捨六入',
        tobashita_player_id=None,
    )

    # Assert
    assert isinstance(result, Dict)
    assert len(result) == 4
    assert result['line_user_id1'] == -40
    assert result['line_user_id2'] == -20
    assert result['line_user_id3'] == 10
    assert result['line_user_id4'] == 50


@pytest.fixture(params=[
    (
        {
            'line_user_id1': -10000,
            'line_user_id2': 20000,
            'line_user_id3': 30000,
            'line_user_id4': 60000,
        },
        10,
        None,
        {
            'line_user_id1': -40,
            'line_user_id2': -10,
            'line_user_id3': 0,
            'line_user_id4': 50,
        },
    ),
    (
        {
            'line_user_id1': -10000,
            'line_user_id2': 20000,
            'line_user_id3': 30000,
            'line_user_id4': 60000,
        },
        0,
        'line_user_id4',
        {
            'line_user_id1': -40,
            'line_user_id2': -10,
            'line_user_id3': 0,
            'line_user_id4': 50,
        },
    ),
    (
        {
            'line_user_id1': -10000,
            'line_user_id2': 20000,
            'line_user_id3': 30000,
            'line_user_id4': 60000,
        },
        10,
        'line_user_id3',
        {
            'line_user_id1': -50,
            'line_user_id2': -10,
            'line_user_id3': 10,
            'line_user_id4': 50,
        },
    ),
    (
        {
            'line_user_id1': -10000,
            'line_user_id2': -20000,
            'line_user_id3': 30000,
            'line_user_id4': 60000,
        },
        10,
        'line_user_id3',
        {
            'line_user_id1': -50,
            'line_user_id2': -60,
            'line_user_id3': 20,
            'line_user_id4': 90,
        },
    ),
])
def text_case2(request):
    return request.param


def test_ok_with_tobi(text_case2):
    # Arrange

    # Act
    result = calculate_service.run(
        points=text_case2[0],
        ranking_prize=[0, 0, 0, 0],
        tobi_prize=text_case2[1],
        rounding_method='3万点以下切り上げ/以上切り捨て',
        tobashita_player_id=text_case2[2],
    )

    # Assert
    assert isinstance(result, Dict)
    assert len(result) == 4
    assert result['line_user_id1'] == text_case2[3]['line_user_id1']
    assert result['line_user_id2'] == text_case2[3]['line_user_id2']
    assert result['line_user_id3'] == text_case2[3]['line_user_id3']
    assert result['line_user_id4'] == text_case2[3]['line_user_id4']

