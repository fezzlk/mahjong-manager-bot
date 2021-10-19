"""calculate"""

from .interfaces.ICalculateService import ICalculateService
from typing import Dict, List
from server import logger


class CalculateService(ICalculateService):

    def run_calculate(
        self,
        points: Dict[str, int],
        ranking_prize: List[int],
        tobi_prize: int = 0,
        rounding_method: str = None,
        tobashita_player_id: str = None,
    ) -> Dict[str, int]:
        # 準備
        sorted_points = sorted(
            points.items(), key=lambda x: x[1], reverse=True)
        # TODO:ソートしない（高順位が高得点前提にしない）
        sorted_prize = sorted(
            ranking_prize,
            reverse=True,
        )

        # 計算方法合わせて点数調整用の padding を設定
        padding = 0
        if rounding_method == '五捨六入':
            padding = 400
        elif rounding_method == '四捨五入':
            padding = 500
        elif rounding_method == '切り捨て':
            padding = 0
        elif rounding_method == '切り上げ':
            padding = 900

        # 素点計算
        result = {}
        tobasare_players = []
        isTobi = not(tobashita_player_id is None or
                     tobashita_player_id == '')
        # 2~4位
        for t in sorted_points[1:]:
            player = t[0]
            point = t[1]
            # 点数がマイナスの場合、飛ばされたプレイヤーリストに追加する
            if (point < 0):
                tobasare_players.append(player)

            # マイナス点の場合の端数処理を考慮するため、100000足して130(=(100000+30000)/1000)を引く
            result[player] = int((point + 10000 + padding) / 1000) - 130

        # 1位(他プレイヤーの点数合計×(-1))
        result[sorted_points[0][0]] = -1 * sum(result.values())

        # 順位点、飛び賞加算
        for i, t in enumerate(sorted_points):
            # 順位点
            result[t[0]] += sorted_prize[i]
            # 飛び賞
            if isTobi:
                if t[0] in tobasare_players:
                    result[t[0]] -= tobi_prize
                if t[0] == tobashita_player_id:
                    result[t[0]] += tobi_prize * len(tobasare_players)
                else:
                    logger.warning(
                        'tobashita_player_id is not matching'
                    )
        return result
