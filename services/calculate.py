class CalculateService:

    def __init__(self, reply_service, result_service, config_service):
        self.reply_service = reply_service
        self.result_service = result_service
        self.config_service = config_service
        self.points = {}

    def calculate(self):
        if len(self.points) != 4:
            self.reply_service.add('四人分の点数を入力してください。点数を取り消したい場合は @{ユーザー名} と送ってください。')
            return
        if int(sum(self.points.values())/1000) != 100:
            self.reply_service.add(f'点数の合計が{sum(self.points.values())}点です。合計100000点+αになるように修正してください。')
            return
        calc_result = self.run_calculate()
        self.result_service.add_result(calc_result)
        self.result_service.reply_current_result()

    def run_calculate(self):
        sorted_points = sorted(self.points.items(), key=lambda x:x[1])
        result = {}
        for t in sorted_points[:-1]:
            result[t[0]] = int(t[1]/1000) - 30
        result[sorted_points[-1][0]] = -1 * sum(result.values())
        sorted_prize = sorted(self.config_service.prize)
        for i, t in enumerate(sorted_points):
            result[t[0]] = result[t[0]] + sorted_prize[i]
        return result
