from repositories import (
    group_repository,
    group_setting_repository,
    hanchan_repository,
    match_repository,
    user_repository,
    web_user_repository,
)
from use_cases.create_dummy_use_case import CreateDummyUseCase


def test_create_dummy_use_case():
    # 目的: test_create_dummy_use_case の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: users の件数が 10 件 / web_users の件数が 4 件 / groups の件数が 5 件 / groups_settings の件数が 3 件 / hanchans の件数が 2 件 / matches の件数が 2 件
    # reply_service: なし
    # DB操作: users = user_repository.find(); web_users = web_user_repository.find(); groups = group_repository.find(); groups_settings = group_setting_repository.find(); matches = match_repository.find(); hanchans = hanchan_repository.find()
    # Act
    CreateDummyUseCase().execute()

    # Assert
    users = user_repository.find()
    web_users = web_user_repository.find()
    groups = group_repository.find()
    groups_settings = group_setting_repository.find()
    matches = match_repository.find()
    hanchans = hanchan_repository.find()

    assert len(users) == 10
    assert len(web_users) == 4
    assert len(groups) == 5
    assert len(groups_settings) == 3
    assert len(hanchans) == 2
    assert len(matches) == 2
