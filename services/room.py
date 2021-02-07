"""room"""

from enum import Enum
from models import Rooms


class Modes(Enum):
    """mode"""

    wait = 'wait'
    input = 'input'
    delete = 'delete'


class RoomService:
    """room service"""

    def __init__(self, services):
        self.services = services
        self.modes = Modes

    def register(self):
        """register"""

        room_id = self.services.app_service.req_room_id
        if room_id == None:
            return
        room = self.services.app_service.db.session\
            .query(Rooms).filter(Rooms.room_id == room_id).first()
        if room == None:
            room = Rooms(room_id=room_id,
                         mode=self.modes.wait.value,
                         )
            self.services.app_service.db.session.add(room)
            self.services.app_service.db.session.commit()

    def get():
        room_id = self.services.app_service.req_room_id
        return self.services.app_service.db.session\
            .query(Rooms).filter(Rooms.room_id == room_id).first()

    def chmod(self, mode):
        room_id = self.services.app_service.req_room_id
        if not mode in self.modes:
            self.services.reply_service.add_text(
                'error: 予期しないモード変更リクエストを受け取りました。')
            return

        target = self.services.app_service.db.session\
            .query(Rooms).filter(Rooms.room_id == room_id).first()
        if target == None:
            return
        target.mode = mode.value
        self.services.app_service.db.session.commit()

        if mode == self.modes.input:
            self.services.reply_service.add_text(
                f'第{self.services.matches_service.count_results()+1}回戦お疲れ様です。各自点数を入力してください。\
                \n（同点の場合は上家が高くなるように数点追加してください）')
            return
        else:
            self.services.results_service.drop_active()
        if mode == self.modes.wait:
            self.services.reply_service.add_text(
                f'始める時は「_start」と入力してください。')
            return
        if mode == self.modes.delete:
            self.services.reply_service.add_text(
                '削除したい結果を数字で指定してください。(終了したい場合は _exit)')
            return

    def get_mode(self):
        room_id = self.services.app_service.req_room_id
        target = self.services.app_service.db.session\
            .query(Rooms).filter(Rooms.room_id == room_id).first()
        if target == None:
            return
        return target.mode

    def get_all(self):
        return self.services.app_service.db.session\
            .query(Rooms).all()
