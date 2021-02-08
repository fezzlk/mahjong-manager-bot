"""room"""

from enum import Enum
from models import Rooms


class Modes(Enum):
    """mode"""

    wait = 'wait'
    input = 'input'


class RoomService:
    """room service"""

    def __init__(self, services):
        self.services = services
        self.modes = Modes

    def register(self):
        """register"""

        room_id = self.services.app_service.req_room_id
        if room_id == None:
            self.services.app_service.logger.warning(f'{room_id} is not found')
            return
        room = self.services.app_service.db.session\
            .query(Rooms).filter(Rooms.room_id == room_id).first()
        if room == None:
            room = Rooms(room_id=room_id,
                         mode=self.modes.wait.value,
                         )
            self.services.app_service.db.session.add(room)
            self.services.app_service.db.session.commit()
            self.services.app_service.logger.info(f'create: {room_id}')

    def chmod(self, mode):
        room_id = self.services.app_service.req_room_id
        if not mode in self.modes:
            self.services.reply_service.add_message(
                'error: 予期しないモード変更リクエストを受け取りました。')
            return

        target = self.services.app_service.db.session\
            .query(Rooms).filter(Rooms.room_id == room_id).first()
        if target == None:
            return
        target.mode = mode.value
        self.services.app_service.db.session.commit()

        if mode == self.modes.input:
            self.services.reply_service.add_message(
                f'第{self.services.matches_service.count_results()+1}回戦お疲れ様です。各自点数を入力してください。\
                \n（同点の場合は上家が高くなるように数点追加してください）')
            return
        else:
            self.services.results_service.delete_current()
        if mode == self.modes.wait:
            self.services.reply_service.add_message(
                f'始める時は「_start」と入力してください。')
            return

    def get_mode(self):
        room_id = self.services.app_service.req_room_id
        target = self.services.app_service.db.session\
            .query(Rooms).filter(Rooms.room_id == room_id).first()
        if target == None:
            return
        return target.mode

    def get(self, target_ids=None):
        if target_ids is None:
            return self.services.app_service.db.session\
                .query(Rooms)\
                .order_by(Rooms.id)\
                .all()
        if type(target_ids) != list:
            target_ids = [target_ids]
        return self.services.app_service.db.session\
            .query(Rooms).filter(Rooms.id.in_(target_ids))\
            .order_by(Rooms.id).all()

    def delete(self, target_ids):
        if type(target_ids) != list:
            target_ids = [target_ids]
        self.services.app_service.db.session\
            .query(Rooms).filter(
                Rooms.id.in_(target_ids),
            ).delete(synchronize_session=False)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_ids}')
