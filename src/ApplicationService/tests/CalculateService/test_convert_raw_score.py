from typing import Dict

import pytest

from ApplicationService import (
    calculate_service,
)


@pytest.fixture(params=[
    (
        [
            ("line_user_id1", 40000),
            ("line_user_id2", 30000),
            ("line_user_id3", 20000),
            ("line_user_id4", 10000),
        ],
        {
            "line_user_id1": 30,
            "line_user_id2": 0,
            "line_user_id3": -10,
            "line_user_id4": -20,
        },
    ),
    (
        [
            ("line_user_id1", 40001),
            ("line_user_id2", 30001),
            ("line_user_id3", 29999),
            ("line_user_id4", -19999),
        ],
        {
            "line_user_id1": 49,
            "line_user_id2": 0,
            "line_user_id3": 0,
            "line_user_id4": -49,
        },
    ),
])
def text_case1(request):
    return request.param


def test_ok_rounding_method1(text_case1):
    # Arrange

    # Act
    result, _ = calculate_service.convert_raw_score(
        sorted_points=text_case1[0],
        rounding_method="3万点以下切り上げ/以上切り捨て",
    )

    # Assert
    assert isinstance(result, Dict)
    assert len(result) == 4
    for k, v in result.items():
        assert v == text_case1[1][k]


@pytest.fixture(params=[
    (
        [
            ("line_user_id1", 40000),
            ("line_user_id2", 30000),
            ("line_user_id3", 20000),
            ("line_user_id4", 10000),
        ],
        {
            "line_user_id1": 30,
            "line_user_id2": 0,
            "line_user_id3": -10,
            "line_user_id4": -20,
        },
    ),
    (
        [
            ("line_user_id1", 38801),
            ("line_user_id2", 30600),
            ("line_user_id3", 20599),
            ("line_user_id4", 10000),
        ],
        {
            "line_user_id1": 29,
            "line_user_id2": 1,
            "line_user_id3": -10,
            "line_user_id4": -20,
        },
    ),
    (
        [
            ("line_user_id1", 80401),
            ("line_user_id2", 40400),
            ("line_user_id3", -10400),
            ("line_user_id4", -10401),
        ],
        {
            "line_user_id1": 71,
            "line_user_id2": 10,
            "line_user_id3": -40,
            "line_user_id4": -41,
        },
    ),
])
def text_case2(request):
    return request.param


def test_ok_rounding_method2(text_case2):
    # Arrange

    # Act
    result, _ = calculate_service.convert_raw_score(
        sorted_points=text_case2[0],
        rounding_method="五捨六入",
    )

    # Assert
    assert isinstance(result, Dict)
    assert len(result) == 4
    for k, v in result.items():
        assert v == text_case2[1][k]


@pytest.fixture(params=[
    (
        [
            ("line_user_id1", 40000),
            ("line_user_id2", 30000),
            ("line_user_id3", 20000),
            ("line_user_id4", 10000),
        ],
        {
            "line_user_id1": 30,
            "line_user_id2": 0,
            "line_user_id3": -10,
            "line_user_id4": -20,
        },
    ),
    (
        [
            ("line_user_id1", 39001),
            ("line_user_id2", 30500),
            ("line_user_id3", 20499),
            ("line_user_id4", 10000),
        ],
        {
            "line_user_id1": 29,
            "line_user_id2": 1,
            "line_user_id3": -10,
            "line_user_id4": -20,
        },
    ),
    (
        [
            ("line_user_id1", 80501),
            ("line_user_id2", 40500),
            ("line_user_id3", -10500),
            ("line_user_id4", -10501),
        ],
        {
            "line_user_id1": 70,
            "line_user_id2": 11,
            "line_user_id3": -40,
            "line_user_id4": -41,
        },
    ),
])
def text_case3(request):
    return request.param


def test_ok_rounding_method3(text_case3):
    # Arrange

    # Act
    result, _ = calculate_service.convert_raw_score(
        sorted_points=text_case3[0],
        rounding_method="四捨五入",
    )

    # Assert
    assert isinstance(result, Dict)
    assert len(result) == 4
    for k, v in result.items():
        assert v == text_case3[1][k]


@pytest.fixture(params=[
    (
        [
            ("line_user_id1", 40000),
            ("line_user_id2", 30000),
            ("line_user_id3", 20000),
            ("line_user_id4", 10000),
        ],
        {
            "line_user_id1": 30,
            "line_user_id2": 0,
            "line_user_id3": -10,
            "line_user_id4": -20,
        },
    ),
    (
        [
            ("line_user_id1", 38001),
            ("line_user_id2", 31000),
            ("line_user_id3", 20999),
            ("line_user_id4", 10000),
        ],
        {
            "line_user_id1": 29,
            "line_user_id2": 1,
            "line_user_id3": -10,
            "line_user_id4": -20,
        },
    ),
    (
        [
            ("line_user_id1", 80001),
            ("line_user_id2", 40000),
            ("line_user_id3", -10000),
            ("line_user_id4", -10001),
        ],
        {
            "line_user_id1": 71,
            "line_user_id2": 10,
            "line_user_id3": -40,
            "line_user_id4": -41,
        },
    ),
])
def text_case4(request):
    return request.param


def test_ok_rounding_method4(text_case4):
    # Arrange

    # Act
    result, _ = calculate_service.convert_raw_score(
        sorted_points=text_case4[0],
        rounding_method="切り捨て",
    )

    # Assert
    assert isinstance(result, Dict)
    assert len(result) == 4
    for k, v in result.items():
        assert v == text_case4[1][k]


@pytest.fixture(params=[
    (
        [
            ("line_user_id1", 40000),
            ("line_user_id2", 30000),
            ("line_user_id3", 20000),
            ("line_user_id4", 10000),
        ],
        {
            "line_user_id1": 30,
            "line_user_id2": 0,
            "line_user_id3": -10,
            "line_user_id4": -20,
        },
    ),
    (
        [
            ("line_user_id1", 39999),
            ("line_user_id2", 30001),
            ("line_user_id3", 20000),
            ("line_user_id4", 10000),
        ],
        {
            "line_user_id1": 29,
            "line_user_id2": 1,
            "line_user_id3": -10,
            "line_user_id4": -20,
        },
    ),
    (
        [
            ("line_user_id1", 81999),
            ("line_user_id2", 40000),
            ("line_user_id3", -10999),
            ("line_user_id4", -11000),
        ],
        {
            "line_user_id1": 71,
            "line_user_id2": 10,
            "line_user_id3": -40,
            "line_user_id4": -41,
        },
    ),
])
def text_case5(request):
    return request.param


def test_ok_rounding_method5(text_case5):
    # Arrange

    # Act
    result, _ = calculate_service.convert_raw_score(
        sorted_points=text_case5[0],
        rounding_method="切り上げ",
    )

    # Assert
    assert isinstance(result, Dict)
    assert len(result) == 4
    for k, v in result.items():
        assert v == text_case5[1][k]


@pytest.fixture(params=[
    (
        [
            ("line_user_id1", 40000),
            ("line_user_id2", 30000),
            ("line_user_id3", 20000),
            ("line_user_id4", 10000),
        ],
        [],
    ),
    (
        [
            ("line_user_id1", 50001),
            ("line_user_id2", 30000),
            ("line_user_id3", 20000),
            ("line_user_id4", -1),
        ],
        ["line_user_id4"],
    ),
    (
        [
            ("line_user_id1", 80000),
            ("line_user_id2", 50000),
            ("line_user_id3", -20000),
            ("line_user_id4", -10000),
        ],
        ["line_user_id3", "line_user_id4"],
    ),
])
def text_case6(request):
    return request.param


def test_ok_tobasare_players(text_case6):
    # Arrange

    # Act
    _, tobasare_players = calculate_service.convert_raw_score(
        sorted_points=text_case6[0],
        rounding_method="切り上げ",
    )

    # Assert
    assert len(tobasare_players) == len(text_case6[1])
    for id in text_case6[1]:
        assert id in tobasare_players

