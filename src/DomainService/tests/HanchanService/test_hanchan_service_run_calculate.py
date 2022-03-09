import pytest
from DomainService.HanchanService import HanchanService

dummy_points_list = [
    {'a': 10000, 'b': 20000, 'c': 30000, 'd': 40000},
    {'a': -10000, 'b': 20000, 'c': 30000, 'd': 60000},
    {'a': -10000, 'b': -20000, 'c': 30000, 'd': 100000},
    {'a': -10000, 'b': -5000, 'c': -2000, 'd': 117000},
    {'a': 10000, 'b': 25001, 'c': 25000, 'd': 40000},
    {'a': 10000, 'b': 25000, 'c': 24999, 'd': 40000},
    {'a': 40000, 'b': 30000, 'c': 20000, 'd': 10000},
    {'a': 10100, 'b': 20100, 'c': 30100, 'd': 39700},
    {'a': -10900, 'b': 20100, 'c': 30100, 'd': 60700},
    {'a': 10400, 'b': 20400, 'c': 30400, 'd': 38800},
    {'a': -10600, 'b': 20600, 'c': 30600, 'd': 59400},
    {'a': 10500, 'b': 20500, 'c': 30500, 'd': 38500},
    {'a': -10500, 'b': 20500, 'c': 30500, 'd': 59500},
    {'a': 10600, 'b': 20600, 'c': 30600, 'd': 38200},
    {'a': -10400, 'b': 20600, 'c': 30600, 'd': 59200},
    {'a': 10900, 'b': 20900, 'c': 30900, 'd': 37300},
    {'a': -10100, 'b': 20900, 'c': 30900, 'd': 58300},
]

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

dummy_converted_scores_list = [
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -60, 'b': -20, 'c': 10, 'd': 70},
    {'a': -50, 'b': -20, 'c': 10, 'd': 60},
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -40, 'b': -20, 'c': 10, 'd': 50},
    {'a': -70, 'b': -20, 'c': 20, 'd': 70},
    {'a': -60, 'b': -20, 'c': 10, 'd': 70},
    {'a': -50, 'b': -70, 'c': 10, 'd': 110},
    {'a': -60, 'b': -80, 'c': 30, 'd': 110},
    {'a': -60, 'b': -45, 'c': -22, 'd': 127},
    {'a': -70, 'b': -55, 'c': -32, 'd': 157},
    {'a': -40, 'b': 6, 'c': -15, 'd': 49},
    {'a': -40, 'b': 5, 'c': -15, 'd': 50},
    {'a': 50, 'b': 10, 'c': -20, 'd': -40},
]


@pytest.fixture(params=[
    # index of (
    # dummy_points_list,
    # dummy_ranking_prize_list,
    # dummy_tobi_prizes,
    # dummy_rounding_method,
    # dummy_tobashita_player_ids,
    # dummy_converted_scores_list)
    (0, 0, 0, 0, 0, 0),
    (1, 0, 0, 0, 0, 1),
    (0, 1, 0, 0, 0, 2),
    (0, 0, 1, 0, 0, 3),
    (0, 0, 0, 1, 0, 4),
    (0, 0, 0, 2, 0, 5),
    (0, 0, 0, 3, 0, 6),
    (0, 0, 0, 4, 0, 7),
    (0, 0, 0, 0, 1, 8),
    (1, 0, 1, 0, 1, 9),
    (1, 0, 1, 0, 2, 10),
    (2, 0, 1, 0, 0, 11),
    (2, 0, 1, 0, 1, 12),
    (3, 0, 1, 0, 0, 13),
    (3, 0, 1, 0, 3, 14),
    (4, 0, 0, 0, 0, 15),
    (5, 0, 0, 0, 0, 16),
    (6, 0, 0, 0, 0, 17),
])
def case(request) -> int:
    return request.param


def test_success(case):
    # Arrange
    hanchan_service = HanchanService()

    # Act
    result = hanchan_service.run_calculate(
        points=dummy_points_list[case[0]],
        ranking_prize=dummy_ranking_prize_list[case[1]],
        tobi_prize=dummy_tobi_prizes[case[2]],
        rounding_method=dummy_rounding_method[case[3]],
        tobashita_player_id=dummy_tobashita_player_ids[case[4]],
    )

    # Assert
    expected = dummy_converted_scores_list[case[5]]
    assert len(result) == len(expected)
    for key in result:
        assert result[key] == expected[key]
