"""config"""

from repositories import session_scope
from repositories.configs import ConfigsRepository
from server import logger

DEFAULT_CONFIGS = {'レート': '点3', '順位点': ','.join(['20', '10', '-10', '-20']),
                   '飛び賞': '10', 'チップ': 'なし', '人数': '4',
                   '端数計算方法': '3万点以下切り上げ/以上切り捨て'}


class ConfigService:
    """config service"""

    def get(self, ids=None):
        # config.id を指定してなければ全ての config を取得
        if ids is None:
            with session_scope() as session:
                return ConfigsRepository.find_all(session)

        # id に合致する config を取得
        with session_scope() as session:
            return ConfigsRepository.find_by_ids(session, ids)

    def get_by_key(self, target_id, key):
        # デフォルトから変更されている config の取得
        with session_scope() as session:
            config = ConfigsRepository.find(session, target_id, key)

        # 上記の結果何も返ってこなければデフォルトの config を返す
        if config is None:
            return DEFAULT_CONFIGS[key]

        # 取得した config を返す
        return config.value

    def get_by_target(self, target_id):
        # デフォルト config から変更されている config を取得
        with session_scope() as session:
            customized_configs = ConfigsRepository.find_by_target_id(
                session,
                target_id
            )

            # デフォルト config をセット
            configs = DEFAULT_CONFIGS

            # 変更項目を更新
            for customized_config in customized_configs:
                configs[customized_config.key] = customized_config.value

        return configs

    def update(self, target_id, key, value):
        """更新
        args:
            key: config 名
            value: 値
        """
        with session_scope() as session:
            # 既存の変更の削除
            ConfigsRepository.delete(session, target_id, key)

            # リクエストの value がデフォルト値と異なる場合はレコードを作成
            if value != DEFAULT_CONFIGS[key]:
                ConfigsRepository.create(session, target_id, key, value)

        logger.info(
            f'update:{key}:{value}:{target_id}'
        )

    def delete(self, ids):
        # 配列にサニタイズ
        if type(ids) != list:
            ids = [ids]

        with session_scope() as session:
            ConfigsRepository.delete_by_ids(session, ids)

        logger.info(f'delete: id={ids}')
