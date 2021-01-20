"""calculate"""

import json


class CalculateService:
    """calculate service"""

    def __init__(self, services):
        self.services = services

    def calculate(self, points=None, shooter=None):
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
        if (any((x < 0 for x in points.values()))) & (shooter is None):
            self.services.reply_service.add_shooter_menu(points.keys())
            return
        calc_result = self.run_calculate(points, shooter)
        self.services.results_service.update_result(calc_result)
        self.services.results_service.reply_current_result()
        self.services.matches_service.add_result()
        self.services.room_service.chmod(
            self.services.room_service.modes.wait
        )

    def run_calculate(self, points, shooter=None):
        sorted_points = sorted(points.items(), key=lambda x: x[1])
        result = {}
        shut_players = []
        for t in sorted_points[:-1]:
            result[t[0]] = int((t[1]-30000)/1000)
            if (t[1] < 0):
                shut_players.append(t[0])

        if shooter in result.keys():
            result[shooter] += 10
        result[sorted_points[-1][0]] = -1 * sum(result.values())
        sorted_prize = sorted(self.services.config_service.prize)
        for i, t in enumerate(sorted_points):
            result[t[0]] += sorted_prize[i]
            if t[0] in shut_players:
                result[t[0]] -= 10
            if t[0] == shooter:
                result[t[0]] += 10*len(shut_players)

        return result
