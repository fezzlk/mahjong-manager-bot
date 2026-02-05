from domain_model.entities.group_setting import GroupSetting
from repositories import group_setting_repository
from use_cases.web.get_configs_for_web_use_case import GetConfigsForWebUseCase


def test_execute_returns_configs():
    # 目的: test_execute_returns_configs の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: configs の件数が 2 件
    # reply_service: なし
    # DB操作: group_setting_repository.create(GroupSetting(line_group_id="G1")); group_setting_repository.create(GroupSetting(line_group_id="G2"))
    # Arrange
    group_setting_repository.create(GroupSetting(line_group_id="G1"))
    group_setting_repository.create(GroupSetting(line_group_id="G2"))
    use_case = GetConfigsForWebUseCase()

    # Act
    configs = use_case.execute()

    # Assert
    assert len(configs) == 2


def test_execute_returns_empty_list():
    # 目的: test_execute_returns_empty_list の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: configs が [] である
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = GetConfigsForWebUseCase()

    # Act
    configs = use_case.execute()

    # Assert
    assert configs == []
