"""calculate"""

import json


class CalculateService:
    """calculate service"""

    def __init__(self, services):
        self.services = services

    def calculate(self, points=None, tobashita_player=None):
        """calculate"""
        if points is None:
            result = self.services.results_service.get_current()
            points = json.loads(result.points)

        if len(points) != 4:
            self.services.reply_service.add_text(
                '四人分の点数を入力してください。点数を取り消したい場合は @{ユーザー名} と送ってください。')
            return
        if int(sum(points.values())/100) != 1000:
            self.services.reply_service.add_text(
                f'点数の合計が{sum(points.values())}点です。合計100000点+αになるように修正してください。')
            return
        if len(set(points.values())) != 4:
            self.services.reply_service.add_text(
                f'同点のユーザーがいます。上家が1点でも高くなるよう修正してください。')
            return
        # 飛び賞
        if (any((x < 0 for x in points.values()))) & (tobashita_player is None):
            self.services.reply_service.add_tobi_menu(points.keys())
            return
        calc_result = self.run_calculate(points, tobashita_player)
        self.services.results_service.update_result(calc_result)
        self.services.results_service.reply_current_result()
        self.services.matches_service.add_result()
        self.services.room_service.chmod(
            self.services.room_service.modes.wait
        )

    def run_calculate(self, points, tobashita_player=None):
        # 得点の準備
        sorted_points = sorted(points.items(), key=lambda x: x[1])
        sorted_prize = sorted(
            [int(s) for s in self.services.config_service.get('順位点').split(',')]
        )
        tobi_prize = int(self.services.config_service.get('飛び賞'))
        clac_method = self.services.config_service.get('計算方法')

        # 素点計算
        result = {}
        tobasare_players = []
        disabled_tobi = False
        # 2~4位
        for t in sorted_points[:-1]:
            if clac_method == '五捨六入':
                result[t[0]] = int((t[1]+70400)/1000)-100
            if clac_method == '四捨五入':
                result[t[0]] = int((t[1]+70500)/1000)-100
            if clac_method == '切り捨て':
                result[t[0]] = int((t[1]+70000)/1000)-100
            if clac_method == '切り上げ':
                result[t[0]] = int((t[1]+70900)/1000)-100
            else:
                result[t[0]] = int((t[1]-30000)/1000)
            if (t[1] < 0):
                if t[0] == tobashita_player:
                    disabled_tobi = True
                else:
                    tobasare_players.append(t[0])
        # 1位
        result[sorted_points[-1][0]] = -1 * sum(result.values())

        # 順位点、飛び賞加算
        for i, t in enumerate(sorted_points):
            result[t[0]] += sorted_prize[i]
            if disabled_tobi == False:
                if t[0] in tobasare_players:
                    result[t[0]] -= tobi_prize
                if t[0] == tobashita_player:
                    result[t[0]] += tobi_prize*len(tobasare_players)
        return result
