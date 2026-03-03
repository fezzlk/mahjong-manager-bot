from domain_model.entities.group import Group, GroupMode
from repositories import group_repository
from use_cases.web.get_configs_for_web_use_case import GetConfigsForWebUseCase


def test_execute_returns_configs():
    # 目的: グループが 2 件存在する場合に configs が 2 件返ること
    # 入力: group_repository に G1, G2 を作成
    # 想定出力: configs の件数が 2 件
    # Arrange
    group_repository.create(Group(line_group_id="G1", mode=GroupMode.wait.value))
    group_repository.create(Group(line_group_id="G2", mode=GroupMode.wait.value))
    use_case = GetConfigsForWebUseCase()

    # Act
    configs = use_case.execute()

    # Assert
    assert len(configs) == 2
    assert all(isinstance(c, dict) for c in configs)
    assert all("_id" in c for c in configs)


def test_execute_returns_empty_list():
    # 目的: グループが 0 件の場合に空リストが返ること
    # 入力: なし
    # 想定出力: configs が [] である
    # Arrange
    use_case = GetConfigsForWebUseCase()

    # Act
    configs = use_case.execute()

    # Assert
    assert configs == []
