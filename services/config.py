"""config"""

from models import Configs
from sqlalchemy import and_


class ConfigService:
    """config service"""

    def __init__(self, services):
        self.services = services
        self.prize = ['20', '10', '-10', '-20']
        self.configs = {'レート': '点3', '順位点': ','.join(self.prize),
                        '飛び賞': '10', 'チップ': 'なし', '人数': '4',
                        '計算方法': '3万点以下切り上げ/以上切り捨て'}

    def get_by_target(self):
        customed_configs = self.services.app_service.db.session\
            .query(Configs)\
            .filter(Configs.target_id == self.services.app_service.req_room_id)\
            .all()
        configs = self.configs
        for config in customed_configs:
            configs[config.key] = config.value
        return configs

    def reply(self):
        configs = self.get_by_target()
        s = [f'{key}: {str(value)}' for key, value in configs.items()]
        self.services.reply_service.add_message('[設定]\n' + '\n'.join(s))

    def get_by_key(self, key):
        target_id = self.services.app_service.req_room_id
        config = self.services.app_service.db.session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .first()
        if config is None:
            return self.configs[key]
        return config.value

    def update(self, key, value):
        target_id = self.services.app_service.req_room_id
        self.services.app_service.db.session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .delete()
        if value != self.configs[key]:
            config = Configs(
                target_id=target_id,
                key=key,
                value=value,
            )
            self.services.app_service.db.session.add(config)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'update:{key}:{value}:{target_id}')
        self.services.reply_service.add_message(f'{key}を{value}に変更しました。')

    def get(self, target_ids=None):
        if target_ids is None:
            return self.services.app_service.db.session\
                .query(Configs)\
                .order_by(Configs.id)\
                .all()
        if type(target_ids) != list:
            target_ids = [target_ids]
        return self.services.app_service.db.session\
            .query(Configs).filter(Configs.id.in_(target_ids))\
            .order_by(Configs.id).all()

    def delete(self, target_ids):
        if type(target_ids) != list:
            target_ids = [target_ids]
        self.services.app_service.db.session\
            .query(Configs).filter(
                Configs.id.in_(target_ids),
            ).delete(synchronize_session=False)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_ids}')
