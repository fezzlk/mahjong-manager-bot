from dataclasses import dataclass
from typing import List, Optional

RATE_LIST = [0, 1, 2, 3, 4, 5, 10]
TIP_RATE_LIST = [0, 10]
NUM_OF_PLAYERS_LIST = [3, 4]
RANKING_PRIZE_LIST = [
    ['20', '10', '-10', '-20'],
    ['30', '10', '-10', '-30'],
]
ROUNDING_METHOD_LIST = [
    '3万点以下切り上げ/以上切り捨て',
    '五捨六入',
    '四捨五入',
    '切り捨て',
    '切り上げ',
]


@dataclass()
class GroupSetting:
    _id: Optional[int]
    line_group_id: str
    rate: int
    ranking_prize: List[int]
    tip_rate: int
    tobi_prize: int
    num_of_players: int
    rounding_method: int

    def __init__(
        self,
        line_group_id,
        rate=0,
        ranking_prize=[20, 10, -10, -20],
        tip_rate=0,
        tobi_prize=10,
        num_of_players=4,
        rounding_method=0,
        _id: Optional[int] = None,
    ):
        self._id = _id
        self.line_group_id = line_group_id
        self.rate = rate
        self.ranking_prize = ranking_prize
        self.tip_rate = tip_rate
        self.tobi_prize = tobi_prize
        self.num_of_players = num_of_players
        self.rounding_method = rounding_method
