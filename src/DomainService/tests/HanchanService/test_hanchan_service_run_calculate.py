import pytest
from DomainService.HanchanService import HanchanService

dummy_points_list = [{'a': 10000, 'b': 20000, 'c': 30000, 'd': 40000}]

dummy_ranking_prize_list = [
    [20, 10, -10, -20],
    [30, 10, -10, -30],
]

dummy_tobi_prizes = [0, 10]

dummy_rounding_method = [
    '3万点以下切り上げ/以上切り捨て',
    '五捨六入',
    '四捨五入',
    '切り捨て',
    '切り上げ',
]

dummy_tobashita_player_ids = [None, 'c', 'a', 'd']


dummy_points_list1 = [
    {'a': 10000, 'b': 20000, 'c': 30000, 'd': 40000},
    {'a': -10000, 'b': 20000, 'c': 30000, 'd': 60000},
    {'a': 10000, 'b': 25001, 'c': 25000, 'd': 40000},
    {'a': 10000, 'b': 25000, 'c': 24999, 'd': 40000},
    {'a': 40000, 'b': 30000, 'c': 20000, 'd': 10000},
]

dummy_converted_scores_list1 = [
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -60, 'b': -20, 'c': 10, 'd': 70},
    {'a': -40, 'b': 5, 'c': -15, 'd': 50},
    {'a': -40, 'b': 5, 'c': -15, 'd': 50},
    {'a': 50, 'b': 10, 'c': -20, 'd': -40},
]


@pytest.fixture(params=[
    # index of (
    # dummy_points_list,
    # dummy_converted_scores_list)
    (0, 0),
    (1, 1),
    # (2, 2), # FIXME: 同点罫線にて、100未満の数値で順番を決めた後、端数は切るようにする
    (3, 3),
    (4, 4),
])
def case1(request) -> int:
    return request.param


def test_success_default(case1):
    # Arrange
    hanchan_service = HanchanService()

    # Act
    result = hanchan_service.run_calculate(
        points=dummy_points_list1[case1[0]],
        ranking_prize=dummy_ranking_prize_list[0],
        tobi_prize=dummy_tobi_prizes[0],
        rounding_method=dummy_rounding_method[0],
        tobashita_player_id=dummy_tobashita_player_ids[0],
    )

    # Assert
    expected = dummy_converted_scores_list1[case1[1]]
    assert len(result) == len(expected)
    for key in result:
        assert result[key] == expected[key]


dummy_converted_scores_list2 = [
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -50, 'b': -20, 'c': 10, 'd': 60},
]


@pytest.fixture(params=[
    # index of (
    # dummy_ranking_prize_list,
    # dummy_converted_scores_list)
    (0, 0),
    (1, 1),
])
def case2(request) -> int:
    return request.param


def test_success_with_ranking_prize_list(case2):
    # Arrange
    hanchan_service = HanchanService()

    # Act
    result = hanchan_service.run_calculate(
        points=dummy_points_list[0],
        ranking_prize=dummy_ranking_prize_list[case2[0]],
        tobi_prize=dummy_tobi_prizes[0],
        rounding_method=dummy_rounding_method[0],
        tobashita_player_id=dummy_tobashita_player_ids[0],
    )

    # Assert
    expected = dummy_converted_scores_list2[case2[1]]
    assert len(result) == len(expected)
    for key in result:
        assert result[key] == expected[key]


dummy_points_list3 = [
    {'a': 10000, 'b': 20000, 'c': 30000, 'd': 40000},
    {'a': -10000, 'b': 20000, 'c': 30000, 'd': 60000},
    {'a': -10000, 'b': -20000, 'c': 30000, 'd': 100000},
    {'a': -10000, 'b': -5000, 'c': -2000, 'd': 117000},
]

dummy_converted_scores_list3 = [
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -70, 'b': -20, 'c': 20, 'd': 70},
    {'a': -60, 'b': -20, 'c': 10, 'd': 70},
    {'a': -50, 'b': -70, 'c': 10, 'd': 110},
    {'a': -60, 'b': -80, 'c': 30, 'd': 110},
    {'a': -60, 'b': -45, 'c': -22, 'd': 127},
    {'a': -70, 'b': -55, 'c': -32, 'd': 157},
]


@pytest.fixture(params=[
    # index of (
    # dummy_points_list,
    # dummy_tobi_prizes,
    # dummy_tobashita_player_ids,
    # dummy_converted_scores_list)
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 1, 1, 0),
    (1, 1, 1, 1),
    (1, 1, 2, 2),
    (2, 1, 0, 3),
    (2, 1, 1, 4),
    (3, 1, 0, 5),
    (3, 1, 3, 6),
])
def case3(request) -> int:
    return request.param


def test_success_with_tobi(case3):
    # Arrange
    hanchan_service = HanchanService()

    # Act
    result = hanchan_service.run_calculate(
        points=dummy_points_list3[case3[0]],
        ranking_prize=dummy_ranking_prize_list[0],
        tobi_prize=dummy_tobi_prizes[case3[1]],
        rounding_method=dummy_rounding_method[0],
        tobashita_player_id=dummy_tobashita_player_ids[case3[2]],
    )

    # Assert
    expected = dummy_converted_scores_list3[case3[3]]
    assert len(result) == len(expected)
    for key in result:
        assert result[key] == expected[key]


dummy_points_list4 = [
    {'a': 10000, 'b': 20000, 'c': 30000, 'd': 40000},
    {'a': -10000, 'b': 20000, 'c': 30000, 'd': 60000},
    {'a': 10100, 'b': 20100, 'c': 30100, 'd': 39700},
    {'a': -9900, 'b': 20100, 'c': 30100, 'd': 59700},
    {'a': 10400, 'b': 20400, 'c': 30400, 'd': 38800},
    {'a': -9600, 'b': 20400, 'c': 30400, 'd': 58400},
    {'a': 10500, 'b': 20500, 'c': 30500, 'd': 38500},
    {'a': -9500, 'b': 20500, 'c': 30500, 'd': 58500},
    {'a': 10600, 'b': 20600, 'c': 30600, 'd': 38200},
    {'a': -9400, 'b': 20600, 'c': 30600, 'd': 58200},
    {'a': 9900, 'b': 19900, 'c': 29900, 'd': 39700},
    {'a': -10100, 'b': 19900, 'c': 29900, 'd': 57300},
]

dummy_converted_scores_list4 = [
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -60, 'b': -20, 'c': 10, 'd': 70},
    {'a': -39, 'b': -19, 'c': 11, 'd': 47},
    {'a': -59, 'b': -19, 'c': 11, 'd': 67},
    {'a': -41, 'b': -21, 'c': 9, 'd': 53},
    {'a': -61, 'b': -21, 'c': 9, 'd': 73},
]


@pytest.fixture(params=[
    # index of (
    # dummy_points_list,
    # dummy_rounding_method,
    # dummy_converted_scores_list)
    (6, 1, 0),
    (7, 1, 1),
    (8, 1, 2),
    (9, 1, 3),
    (4, 2, 0),
    (5, 2, 1),
    (6, 2, 2),
    (7, 2, 3),
    (0, 3, 0),
    (1, 3, 1),
    (10, 3, 4),
    (11, 3, 5),
    (0, 4, 0),
    (1, 4, 1),
    (2, 4, 2),
    (3, 4, 3),
])
def case4(request) -> int:
    return request.param


def test_success_with_other_rounding_method(case4):
    # Arrange
    hanchan_service = HanchanService()

    # Act
    result = hanchan_service.run_calculate(
        points=dummy_points_list4[case4[0]],
        ranking_prize=dummy_ranking_prize_list[0],
        tobi_prize=dummy_tobi_prizes[0],
        rounding_method=dummy_rounding_method[case4[1]],
        tobashita_player_id=dummy_tobashita_player_ids[0],
    )

    # Assert
    expected = dummy_converted_scores_list4[case4[2]]
    assert len(result) == len(expected)
    for key in result:
        assert result[key] == expected[key]
