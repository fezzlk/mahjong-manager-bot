from typing import Dict, List, Tuple
from .interfaces.ICalculateService import ICalculateService
from DomainModel.entities.GroupSetting import ROUNDING_METHOD_LIST


class CalculateService(ICalculateService):
    def run(
        self,
        points: Dict[str, int],
        ranking_prize: List[int],
        tobi_prize: int = 0,
        rounding_method: str = None,
        tobashita_player_id: str = None,
    ) -> Dict[str, int]:
        sorted_points: list[tuple[str, int]] = sorted(
            points.items(), key=lambda x: x[1], reverse=True)
        sorted_prize = sorted(
            ranking_prize,
            reverse=True,
        )

        result, tobasare_players = self.convert_raw_score(
            sorted_points,
            rounding_method=rounding_method,
        )
        isTobi = not (tobashita_player_id is None or tobashita_player_id == '')

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

        return result

    def convert_raw_score(
        self,
        sorted_points: List[Tuple[str, int]],
        rounding_method: str = None,
    ) -> Tuple[Dict[str, int], List[str]]:
        converted_score = {}
        tobasare_players = []

        # 計算方法に合わせて点数調整用の adjuster(丸めの境界値の調整) と padding(端数調整) を設定
        padding = 0
        adjuster = 100000
        # 五捨六入
        if rounding_method == ROUNDING_METHOD_LIST[1]:
            padding = 400
        # 四捨五入
        elif rounding_method == ROUNDING_METHOD_LIST[2]:
            padding = 500
        # 切り捨て
        elif rounding_method == ROUNDING_METHOD_LIST[3]:
            padding = 0
        # 切り上げ
        elif rounding_method == ROUNDING_METHOD_LIST[4]:
            padding = 999
        # 3万点以下切り上げ/以上切り捨て
        else:
            adjuster = -30000

        # 2~4位
        for t in sorted_points[1:]:
            player = t[0]
            point = t[1]
            # 点数がマイナスの場合、飛ばされたプレイヤーリストに追加する
            if (point < 0):
                tobasare_players.append(player)

            # 3万点切り上げ切り捨ての場合、一時的に30000点を引き、int の丸めを利用する
            # ex. 切り上げ: int(-10100/1000) -> -10000, 切り捨て: int(10100/1000) -> 10000
            # その他の場合、マイナス点の場合の丸め方をプラスの丸め方に合わせるため、一時的に100000足す
            converted_score[player] = int(
                (point + adjuster + padding) / 1000) - 30 - (adjuster // 1000)

        # 1位(他プレイヤーの点数合計×(-1))
        converted_score[sorted_points[0][0]] = -1 * sum(converted_score.values())

        return converted_score, tobasare_players
