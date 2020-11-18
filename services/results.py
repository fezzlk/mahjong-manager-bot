class ResultsService:

    def __init__(self, services):
        self.services = services
        self.results = []

    def add(self, result):
        self.results.append(result)

    def drop(self, i):
        if self.count() > i:
            self.results.pop(i)

    def reply_current_result(self):
        self.services.reply_service.add(f'一半荘お疲れ様でした。結果を表示します。')
        self.services.reply_service.add('\n'.join([f'{user}: {point}' for user, point in self.results[-1].items()]))
        self.services.reply_service.add('今回の結果に一喜一憂せず次の戦いに望んでください。')

    def count(self):
        return len(self.results)

    def reset(self):
        self.results = []
        self.services.reply_service.add('結果を全て削除しました。')

    def reply_all(self):
        count = self.count()
        if count == 0:
            self.services.reply_service.add('まだ結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        self.services.reply_service.add('これまでの対戦結果です。(結果を指定して取り消したい場合は _delete, 全削除したい場合は _reset)')
        for i in range(count):
            self.services.reply_service.add(f'第{i+1}回\n' + '\n'.join([f'{user}: {point}' for user, point in self.results[i].items()]))
        sum = self.get_sum()
        self.services.reply_service.add('総計\n' + '\n'.join([f'{user}: {point}' for user, point in sum.items()]))
        
    def finish(self):
        count = self.count()
        if count == 0:
            self.services.reply_service.add('まだ結果がありません。メニューの結果入力を押して結果を追加してください。')
            return
        self.services.matches_service.add(self.results)
        self.services.reply_service.add('今回の総計を表示します。')
        self.reply_sum_and_money()

    def reply_sum_and_money(self, results=None):
        if results == None:
            results = self.results
        sum = self.get_sum(results)
        self.services.reply_service.add('\n'.join([f'{user}: {point}' for user, point in sum.items()]))
        self.services.reply_service.add('\n'.join([f'{user}: {point * self.services.config_service.get_rate()}円' for user, point in sum.items()]))

    def get_sum(self, results=None):
        if results == None:
            results = self.results
        sum_result = {}
        for res in results:
            for name, point in res.items():
                sum_result[name] += point
        return sum_result