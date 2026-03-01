"""Domain-level constants shared across entities and use cases."""

from enum import IntEnum

RATE_LIST = [0, 1, 2, 3, 4, 5, 10]
CHIP_RATE_LIST = [0, 1]
NUM_OF_PLAYERS_LIST = [3, 4]
RANKING_PRIZE_LIST = [
    ["20", "10", "-10", "-20"],
    ["30", "10", "-10", "-30"],
]
ROUNDING_METHOD_LIST = [
    "3万点以下切り上げ/以上切り捨て",
    "五捨六入",
    "四捨五入",
    "切り捨て",
    "切り上げ",
]


class RoundingMethod(IntEnum):
    """端数計算方法を表す列挙型。整数インデックスと互換性を持つ。"""

    special_rule = 0   # 3万点以下切り上げ/以上切り捨て
    go_san_roku = 1    # 五捨六入
    go_sha_go_nyu = 2  # 四捨五入
    floor = 3          # 切り捨て
    ceil = 4           # 切り上げ
