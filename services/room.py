from enum import Enum


class Modes(Enum):
    wait = 'wait'
    input = 'input'
    off = 'off'
    delete = 'delete'


class RoomService:

    def __init__(self, services):
        self.services = services
        self.modes = Modes
        self.rooms = {}

    def register(self):
        room_id = self.services.app_service.req_room_id
        if room_id:
            self.rooms[room_id] = {}
            self.rooms[room_id]['mode'] = self.modes.wait
            self.rooms[room_id]['points'] = {}
            self.rooms[room_id]['results'] = []

    def chmod(self, mode):
        room_id = self.services.app_service.req_room_id
        if not mode in self.modes:
            self.services.reply_service.add_text(
                'error: 予期しないモード変更リクエストを受け取りました。')
            return
        self.rooms[room_id]['mode'] = mode
        if self.rooms[room_id]['mode'] == self.modes.input:
            self.services.reply_service.add_text(
                f'第{self.services.results_service.count()+1}回戦お疲れ様です。各自点数を入力してください。（同点の場合は上家が高くなるように数点追加してください）')
            return
        elif self.rooms[room_id]['mode'] == self.modes.wait:
            self.services.reply_service.add_text(
                f'こんにちは。快適な麻雀生活の提供に努めます。今日のラッキー牌は「{self.services.app_service.get_random_hai()}」です。')
            return
        elif self.rooms[room_id]['mode'] == self.modes.off:
            self.services.reply_service.add_text(
                '会話に参加しないようにします。私を使いたい時は _on と送信してください。')
            return
        elif self.rooms[room_id]['mode'] == self.modes.delete:
            self.services.reply_service.add_text(
                '削除したい結果を数字で指定してください。(終了したい場合は _exit)')
            self.services.points_service.reply_results()
            return

    def get_mode(self):
        room_id = self.services.app_service.req_room_id
        return self.rooms[room_id]['mode']

    def reply_mode(self):
        room_id = self.services.app_service.req_room_id
        self.services.reply_service.add_text(self.rooms[room_id]['mode'].value)
