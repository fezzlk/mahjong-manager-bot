from domain_model.entities.group import Group
from repositories import group_repository
from use_cases.web.get_groups_for_web_use_case import GetGroupsForWebUseCase


def test_execute_returns_groups():
    # 目的: test_execute_returns_groups の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: groups の件数が 2 件
    # reply_service: なし
    # DB操作: group_repository.create(Group(line_group_id="G1")); group_repository.create(Group(line_group_id="G2"))
    # Arrange
    group_repository.create(Group(line_group_id="G1"))
    group_repository.create(Group(line_group_id="G2"))
    use_case = GetGroupsForWebUseCase()

    # Act
    groups = use_case.execute()

    # Assert
    assert len(groups) == 2


def test_execute_returns_empty_list():
    # 目的: test_execute_returns_empty_list の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: groups が [] である
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = GetGroupsForWebUseCase()

    # Act
    groups = use_case.execute()

    # Assert
    assert groups == []
