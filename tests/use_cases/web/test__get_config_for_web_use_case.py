from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from repositories import group_repository
from use_cases.web.get_config_for_web_use_case import GetConfigForWebUseCase


def test_execute_returns_config_by_line_group_id():
    # 目的: line_group_id でグループの設定を取得できること
    # 入力: G1 グループを作成
    # 想定出力: config is not None / EmbeddedGroupSettings インスタンスである
    # Arrange
    group_repository.create(Group(line_group_id="G1", mode=GroupMode.wait.value))
    use_case = GetConfigForWebUseCase()

    # Act
    config = use_case.execute("G1")

    # Assert
    assert config is not None
    assert isinstance(config, EmbeddedGroupSettings)


def test_execute_returns_none_for_missing_line_group_id():
    # 目的: 存在しない line_group_id を指定した場合に None が返ること
    # 入力: なし
    # 想定出力: config is None
    # Arrange
    use_case = GetConfigForWebUseCase()

    # Act
    config = use_case.execute("nonexistent_group_id")

    # Assert
    assert config is None
