# from DomainModel.entities.GroupSetting import DEFAULT_CONFIGS
# from .interfaces.IConfigService import IConfigService
# from typing import Dict
# from repositories import session_scope, group_setting_repository
# from DomainModel.entities.GroupSetting import Config


# class ConfigService(IConfigService):

#     def get_value_by_key(
#         self,
#         target_id: str,
#         key: str,
#     ) -> str:
#         # デフォルトから変更されている config の取得
#         with session_scope() as session:
#             config = group_setting_repository.find_one_by_target_id_and_key(
#                 session,
#                 target_id,
#                 key
#             )

#         # 上記の結果何も返ってこなければデフォルトの config を返す
#         if config is None:
#             return DEFAULT_CONFIGS[key]

#         # 取得した config を返す
#         return config.value

#     def get_current_settings_by_target(
#         self,
#         target_id: str,
#     ) -> Dict[str, str]:
#         # デフォルト config から変更されている config を取得
#         with session_scope() as session:
#             customized_configs = group_setting_repository.find_by_target_id(
#                 session,
#                 target_id,
#             )

#             # デフォルト config をセット
#             configs = DEFAULT_CONFIGS.copy()

#             # 変更項目を更新
#             for customized_config in customized_configs:
#                 configs[customized_config.key] = customized_config.value

#         return configs

#     def update_setting(
#         self,
#         target_id: str,
#         key: str,
#         value: str,
#     ) -> None:
#         """更新
#         description: レコード自体の更新は行わなず、新たなレコードに作り直す（デフォルト値の場合にレコードを作らないようにするため）
#         args:
#             key: config 名
#             value: 値
#         """
#         with session_scope() as session:
#             # 既存の変更の削除
#             group_setting_repository.delete_by_target_id_and_key(
#                 session, target_id, key)

#             # リクエストの value がデフォルト値と異なる場合はレコードを作成
#             if value != DEFAULT_CONFIGS[key]:
#                 new_config = Config(
#                     target_id,
#                     key,
#                     value,
#                 )
#                 group_setting_repository.create(session, new_config)

#         print(
#             f'update setting of "{target_id}": {key}:{value}'
#         )
