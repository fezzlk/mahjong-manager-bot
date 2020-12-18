"""config"""

from models import Configs
from sqlalchemy import and_


class ConfigService:
    """config service"""

    def __init__(self, services):
        self.services = services
        self.prize = [30, 10, -10, -30]
        self.configs = {'レート': '点3', '順位点': str(
            self.prize), '飛び賞': 'なし', 'チップ': 'なし', '人数': 4}

    def get_by_target(self):
        # configs = self.services.app_service.db.session\
        #     .query(Configs)\
        #     .filter(Configs.target_id == self.services.app_service.req_room_id)\
        #     .all()
        # print(configs)
        # for config in configs:
        #     pring(config)
        configs = self.configs
        return configs

    def reply(self):
        configs = self.get_by_target()
        s = [f'{key}: {value}' for key, value in configs.items()]
        self.services.reply_service.add_text('[設定]\n' + '\n'.join(s))

    def get_rate(self):
        configs = self.get_by_target()
        return int(configs['レート'][1:]) * 10

    def update(self, key, value, insert=True):
        config = self.services.app_service.db.session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == self.services.app_service.req_room_id,
                Configs.key == key,
                Configs.value == value,
            ))\
            .first()
        if config == None:
            if insert == True:
                self.add(key, value)
            return
        config.value = value
        self.services.app_service.db.session.commit()

    def add(self, key, value):
        config = Configs(target_id=self.services.app_service.req_room_id,
                         key=key,
                         value=value,
                         )
        self.services.app_service.db.session.add(config)
        self.services.app_service.db.session.commit()
