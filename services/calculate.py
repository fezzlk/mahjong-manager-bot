"""calculate"""


class CalculateService:
    """calculate service"""

    def __init__(self, services):
        self.services = services

    def calculate(self, points=None):
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
        calc_result = self.run_calculate(points)
        self.services.results_service.add(calc_result)
        self.services.results_service.reply_current_result()

    def run_calculate(self, points):
        sorted_points = sorted(points.items(), key=lambda x: x[1])
        result = {}
        for t in sorted_points[:-1]:
            result[t[0]] = int(t[1]/1000) - 30
        result[sorted_points[-1][0]] = -1 * sum(result.values())
        sorted_prize = sorted(self.services.config_service.prize)
        for i, t in enumerate(sorted_points):
            result[t[0]] = result[t[0]] + sorted_prize[i]
        return result
