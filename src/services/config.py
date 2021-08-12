"""config"""

from models import Configs
from sqlalchemy import and_

DEFAULT_CONFIGS = {'レート': '点3', '順位点': ','.join(['20', '10', '-10', '-20']),
                   '飛び賞': '10', 'チップ': 'なし', '人数': '4',
                   '端数計算方法': '3万点以下切り上げ/以上切り捨て'}


class ConfigService:
    """config service"""

    def __init__(self, services):
        self.services = services
        self.configs = DEFAULT_CONFIGS

        """get all configs by ids
        """
    def get(self, target_ids=None):
        # config.id を指定してなければ全ての config を取得
        if target_ids is None:
            return self.services.app_service.db.session\
                .query(Configs)\
                .order_by(Configs.id)\
                .all()
        # 配列にサニタイズ
        if type(target_ids) != list:
            target_ids = [target_ids]
        # id に合致する config を取得
        return self.services.app_service.db.session\
            .query(Configs).filter(Configs.id.in_(target_ids))\
            .order_by(Configs.id).all()

        """key を元にリクエスト元ルームの config を返す
        """
    def get_by_key(self, key):
        # リクエスト元ルームIDの取得
        target_id = self.services.app_service.req_room_id
        
        # デフォルトから変更されている config の取得
        config = self.services.app_service.db.session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .first()

        # 上記の結果何も返ってこなければデフォルトの config を返す
        if config is None:
            return self.configs[key]

        # 取得した config を返す
        return config.value

        """リクエスト元(ユーザーorルーム)の全ての config を返す
        """
    def get_by_target(self):
        # リクエスト元ルームIDの取得（ルームからのリクエストでなければユーザーID)
        if self.services.app_service.req_room_id is not None:
            target_id = self.services.app_service.req_room_id
        else:
            target_id = self.services.app_service.req_user_id

        # デフォルト config から変更されている config を取得
        customized_configs = self.services.app_service.db.session\
            .query(Configs)\
            .filter(Configs.target_id == target_id)\
            .all()

        # デフォルト config をセット
        configs = self.configs

        # 変更項目を更新
        for config in customized_configs:
            configs[config.key] = config.value

        return configs

        """返信
        """
    def reply(self):
        # 取得
        configs = self.get_by_target()

        # 返信メッセージ用に変換&返信
        s = [f'{key}: {str(value)}' for key, value in configs.items()]
        self.services.reply_service.add_message('[設定]\n' + '\n'.join(s))

        """更新
        args:
            key: config 名
            value: 値
        """
    def update(self, key, value):
        # リクエスト元のルームIDの取得
        target_id = self.services.app_service.req_room_id

        # 既存の変更の削除
        self.services.app_service.db.session\
            .query(Configs)\
            .filter(and_(
                Configs.target_id == target_id,
                Configs.key == key,
            ))\
            .delete()

        # リクエストの value がデフォルト値と異なる場合はレコードを作成
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

    """delete by id
    """
    def delete(self, target_ids):
        # 配列にサニタイズ
        if type(target_ids) != list:
            target_ids = [target_ids]
        self.services.app_service.db.session\
            .query(Configs).filter(
                Configs.id.in_(target_ids),
            ).delete(synchronize_session=False)
        self.services.app_service.db.session.commit()
        self.services.app_service.logger.info(f'delete: id={target_ids}')
