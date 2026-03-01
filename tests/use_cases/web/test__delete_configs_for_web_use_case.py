from domain_model.entities.group_setting import GroupSetting
from repositories import group_setting_repository
from use_cases.web.delete_configs_for_web_use_case import DeleteConfigsForWebUseCase


def test_execute_deletes_configs_by_ids():
    # 目的: test_execute_deletes_configs_by_ids の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: remaining の件数が 1 件 / remaining[0].line_group_id が "G2" である
    # reply_service: なし
    # DB操作: c1 = group_setting_repository.create(GroupSetting(line_group_id="G1")); c2 = group_setting_repository.create(GroupSetting(line_group_id="G2")); remaining = group_setting_repository.find()
    # Arrange
    c1 = group_setting_repository.create(GroupSetting(line_group_id="G1"))
    group_setting_repository.create(GroupSetting(line_group_id="G2"))
    use_case = DeleteConfigsForWebUseCase()

    # Act
    use_case.execute([c1._id])

    # Assert
    remaining = group_setting_repository.find()
    assert len(remaining) == 1
    assert remaining[0].line_group_id == "G2"


def test_execute_with_empty_ids_does_nothing():
    # 目的: test_execute_with_empty_ids_does_nothing の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: remaining の件数が 1 件
    # reply_service: なし
    # DB操作: group_setting_repository.create(GroupSetting(line_group_id="G1")); remaining = group_setting_repository.find()
    # Arrange
    group_setting_repository.create(GroupSetting(line_group_id="G1"))
    use_case = DeleteConfigsForWebUseCase()

    # Act
    use_case.execute([])

    # Assert
    remaining = group_setting_repository.find()
    assert len(remaining) == 1
