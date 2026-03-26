from _web_test_utils import create_app, request_context

from domain_model.entities.group import Group, GroupMode
from repositories import group_repository
from use_cases.web.update_config_for_web_use_case import UpdateConfigForWebUseCase


def test_execute_updates_group_setting_fields():
    # 目的: フォームの値でグループの embedded settings が更新されること
    # 入力: G1 グループを作成し rate=3, rounding_method=2 を送信
    # 想定出力: g1.settings.rate が 3 / g1.settings.rounding_method が 2
    # Arrange
    group_repository.create(Group(line_group_id="G1", mode=GroupMode.wait.value))
    app = create_app()
    use_case = UpdateConfigForWebUseCase()

    form = {
        "line_group_id": "G1",
        "rate": "3",
        "rounding_method": "2",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    g1 = group_repository.find({"line_group_id": "G1"})[0]
    assert g1.settings is not None
    assert g1.settings.rate == 3
    assert g1.settings.rounding_method == 2


def test_execute_with_no_line_group_id_does_nothing():
    # 目的: フォームに line_group_id がない場合は早期 return されること
    # 入力: G1 グループを作成し line_group_id なしのフォームを送信
    # 想定出力: G1 の settings は変わらない (None のまま)
    # Arrange
    group_repository.create(Group(line_group_id="G1", mode=GroupMode.wait.value))
    app = create_app()
    use_case = UpdateConfigForWebUseCase()

    form = {}  # line_group_id なし → 早期 return

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    g1 = group_repository.find({"line_group_id": "G1"})[0]
    assert g1.settings is None
