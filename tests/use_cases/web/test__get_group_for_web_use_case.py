from domain_model.entities.group import Group
from repositories import group_repository
from use_cases.web.get_group_for_web_use_case import GetGroupForWebUseCase


def test_execute_returns_group_by_id():
    # 目的: test_execute_returns_group_by_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: group is not None / group.line_group_id が "G1" である
    # reply_service: なし
    # DB操作: created = group_repository.create(Group(line_group_id="G1"))
    # Arrange
    created = group_repository.create(Group(line_group_id="G1"))
    use_case = GetGroupForWebUseCase()

    # Act
    group = use_case.execute(created._id)

    # Assert
    assert group is not None
    assert group.line_group_id == "G1"


def test_execute_returns_none_for_missing_id():
    # 目的: test_execute_returns_none_for_missing_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: group is None
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = GetGroupForWebUseCase()

    # Act
    group = use_case.execute("000000000000000000000000")

    # Assert
    assert group is None
