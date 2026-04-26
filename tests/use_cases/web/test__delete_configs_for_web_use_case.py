from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from repositories import group_repository
from use_cases.web.delete_configs_for_web_use_case import DeleteConfigsForWebUseCase


def test_execute_clears_settings_by_line_group_ids():
    # 目的: 指定した line_group_id の settings が None にリセットされること
    # 入力: G1, G2 グループを作成し両方に settings を設定
    # 想定出力: G1 の settings は None / G2 の settings は残る
    # Arrange
    settings = EmbeddedGroupSettings(rate=5)
    group_repository.create(Group(line_group_id="G1", mode=GroupMode.wait.value))
    group_repository.create(Group(line_group_id="G2", mode=GroupMode.wait.value))
    group_repository.update({"line_group_id": "G1"}, {"settings": settings.to_dict()})
    group_repository.update({"line_group_id": "G2"}, {"settings": settings.to_dict()})
    use_case = DeleteConfigsForWebUseCase()

    # Act
    use_case.execute(["G1"])

    # Assert
    g1 = group_repository.find({"line_group_id": "G1"})[0]
    g2 = group_repository.find({"line_group_id": "G2"})[0]
    assert g1.settings is None
    assert g2.settings is not None


def test_execute_with_empty_ids_does_nothing():
    # 目的: 空リストを渡した場合に設定が変わらないこと
    # 入力: G1 グループに settings を設定
    # 想定出力: G1 の settings は変わらない
    # Arrange
    settings = EmbeddedGroupSettings(rate=5)
    group_repository.create(Group(line_group_id="G1", mode=GroupMode.wait.value))
    group_repository.update({"line_group_id": "G1"}, {"settings": settings.to_dict()})
    use_case = DeleteConfigsForWebUseCase()

    # Act
    use_case.execute([])

    # Assert
    g1 = group_repository.find({"line_group_id": "G1"})[0]
    assert g1.settings is not None
