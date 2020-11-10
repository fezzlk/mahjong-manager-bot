class ResultsService:

    def __init__(self, reply_service, points_service, config_service):
        self.results = []
        self.reply_service = reply_service
        self.points_service = points_service
        self.config_service = config_service

    def add(self, result):
        self.results.append(result)

    def drop(self, i):
        if len(self.results) > i:
            self.results.pop(i)

    def reply_current_result(self):
        self.reply_service.add(f'一半荘お疲れ様でした。結果を表示します。')
        self.points_service.reply(self.count()-1)
        self.reply_service.add('今回の結果に一喜一憂せず次の戦いに望んでください。(これまでの結果を確認したい場合は @RESULTS と送ってください。)')

    def count(self):
        return len(self.results)

    def reset(self):
        self.results = []
        self.reply_service.add('結果を全て削除しました。')

    def reply(self):
        count = self.count()
        if count == 0:
            self.reply_service.add('まだ結果がありません。@INPUT と送って結果を追加してください。')
            return
        self.reply_service.add('これまでの対戦結果です。(結果を取り消したい場合は @DELETE, 全削除したい場合は @RESET)')
        for i in range(count):
            self.reply_service.add(f'第{i+1}回\n' + '\n'.join(self.results[i]))
        
    def reply_sum_and_money(self):
        count = self.count()
        if count == 0:
            self.reply_service.add('まだ結果がありません。@INPUT と送って結果を追加してください。')
            return
        sum_result = self.get_sum_results()
        self.reply_service.add('今回の総計を表示します。')
        self.reply_service.add('\n'.join([f'{user}: {point}' for user, point in sum_result.items()]))
        self.reply_service.add('\n'.join([f'{user}: {point * self.config_service.get_rate()}円' for user, point in sum_result.items()]))

    def get_sum_results(self):
        sum_result = {}
        for res in self.results:
            for name, point in res.items():
                sum_result[name] += point
        return sum_result