"""config"""

from repositories import session_scope, configs

DEFAULT_CONFIGS = {'レート': '点3', '順位点': ','.join(['20', '10', '-10', '-20']),
                   '飛び賞': '10', 'チップ': 'なし', '人数': '4',
                   '端数計算方法': '3万点以下切り上げ/以上切り捨て'}


class ConfigService:
    """config service"""

    def __init__(self, services):
        self.services = services

        """get all configs by ids
        """
    def get(self, ids=None):
        # config.id を指定してなければ全ての config を取得
        if target_ids is None:
            with session_scope as session:
                return configs.find_all(session)

        # id に合致する config を取得
        with session_scope as session:
            return configs.find_by_ids(session, ids)

        """key を元にリクエスト元ルームの config を返す
        """
    def get_by_key(self, key):
        # リクエスト元ルームIDの取得
        target_id = self.services.app_service.req_room_id
        
        # デフォルトから変更されている config の取得
        with session_scope as session:
            config = configs.find(session, target_id, key)

        # 上記の結果何も返ってこなければデフォルトの config を返す
        if config is None:
            return DEFAULT_CONFIGS[key]

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
        with session_scope as session:
            customized_configs = configs.find_by_target_id(session, target_id)

        # デフォルト config をセット
        configs = DEFAULT_CONFIGS

        # 変更項目を更新
        for customized_config in customized_configs:
            configs[customized_config.key] = customized_config.value

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

        with session_scope as session:
            # 既存の変更の削除
            configs.delete(session, target_id, key)

            # リクエストの value がデフォルト値と異なる場合はレコードを作成
            if value != DEFAULT_CONFIGS[key]:
                configs.create(session, target_id, key, value)

        self.services.app_service.logger.info(f'update:{key}:{value}:{target_id}')
        self.services.reply_service.add_message(f'{key}を{value}に変更しました。')

    """delete by id
    """
    def delete(self, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

        with session_scope as session:
            config.delete_by_ids(session, ids)

        self.services.app_service.logger.info(f'delete: id={ids}')
