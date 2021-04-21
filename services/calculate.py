"""calculate"""

import json


class CalculateService:
    """calculate service"""

    def __init__(self, services):
        self.services = services

    def calculate(self, points=None, tobashita_player_id=None):
        """calculate"""
        if points is None:
            current = self.services.results_service.get_current()
            if current is None:
                self.services.app_service.logger.error(
                    'current points is not found.'
                )
                return
            points = json.loads(current.points)

        if len(points) != 4:
            self.services.reply_service.add_message(
                '四人分の点数を入力してください。点数を取り消したい場合は @{ユーザー名} と送ってください。')
            return
        if int(sum(points.values())/100) != 1000:
            self.services.reply_service.add_message(
                f'点数の合計が{sum(points.values())}点です。合計100000点+αになるように修正してください。')
            return
        if len(set(points.values())) != 4:
            self.services.reply_service.add_message(
                f'同点のユーザーがいます。上家が1点でも高くなるよう修正してください。')
            return
        # 飛び賞
        if (any(x < 0 for x in points.values())) & (tobashita_player_id is None):
            self.services.reply_service.add_tobi_menu(
                [player_id for player_id in points.keys() if points[player_id] > 0]
            )
            return
        calc_result = self.run_calculate(points, tobashita_player_id)
        self.services.results_service.update_result(calc_result)
        self.services.matches_service.add_result()
        self.services.results_service.reply_current_result()
        self.services.results_service.archive()
        self.services.room_service.chmod(
            self.services.room_service.modes.wait
        )

    def run_calculate(self, points, tobashita_player_id=None):
        # 得点の準備
        sorted_points = sorted(
            points.items(), key=lambda x: x[1], reverse=True)
        sorted_prize = sorted(
            [int(s) for s in self.services.config_service.get_by_key(
                '順位点').split(',')],
            reverse=True,
        )
        tobi_prize = int(self.services.config_service.get_by_key('飛び賞'))
        clac_method = self.services.config_service.get_by_key('端数計算方法')

        # 素点計算
        result = {}
        tobasare_players = []
        disabled_tobi = (tobashita_player_id is None) | (
            tobashita_player_id == '')
        # 2~4位
        for t in sorted_points[1:]:
            player = t[0]
            point = t[1]
            # マイナス点の場合の端数処理を考慮し、100000足して130(=100000/1000)を引く
            if clac_method == '五捨六入':
                result[player] = int((point+100400)/1000)-130
            elif clac_method == '四捨五入':
                result[player] = int((point+100500)/1000)-130
            elif clac_method == '切り捨て':
                result[player] = int((point+100000)/1000)-130
            elif clac_method == '切り上げ':
                result[player] = int((point+100900)/1000)-130
            else:
                result[player] = int((point-30000)/1000)
            if (point < 0):
                tobasare_players.append(player)
        # 1位
        result[sorted_points[0][0]] = -1 * sum(result.values())

        # 順位点、飛び賞加算
        for i, t in enumerate(sorted_points):
            result[t[0]] += sorted_prize[i]
            if disabled_tobi == False:
                if t[0] in tobasare_players:
                    result[t[0]] -= tobi_prize
                if t[0] == tobashita_player_id:
                    result[t[0]] += tobi_prize*len(tobasare_players)
                else:
                    self.services.app_service.logger.warning(
                        'tobashita_player_id is not matching'
                    )
        return result
