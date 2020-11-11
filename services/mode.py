from enum import Enum

class Modes(Enum):
    WAIT = 'wait'
    INPUT = 'input'
    OFF = 'off'
    DELETE = 'delete'
    
class ModeService:

    def __init__(self, app_service, reply_service, results_service, points_service):
        self.app_service = app_service
        self.reply_service = reply_service
        self.results_service = results_service
        self.points_service = points_service
        self.modes = Modes
        self.mode = self.modes.WAIT

    def update(self, mode):
        if not mode in self.modes:
            self.reply_service.add('warning: 予期しないモード変更を行おうとしています。')
            return
        self.mode = mode
        if self.mode == self.modes.INPUT:
            self.reply_service.add(f'第{self.results_service.count()+1}回戦お疲れ様です。各自点数を入力してください。（同点の場合は上家が高くなるように数点追加してください）')
            return
        elif self.mode == self.modes.WAIT:
            self.reply_service.add(f'こんにちは。快適な麻雀生活の提供に努めます。今日のラッキー牌は「{self.app_service.get_random_hai()}」です。')
            return
        elif self.mode == self.modes.OFF:
            self.reply_service.add('会話に参加しないようにします。私を使いたい時は _on と送信してください。')
            return
        elif self.mode == self.modes.DELETE:
            self.reply_service.add('削除したい結果を数字で指定してください。(終了したい場合は _exit)')
            self.points_service.reply_results()
            return

    def reply(self):
        self.reply_service.add(self.mode.value)

