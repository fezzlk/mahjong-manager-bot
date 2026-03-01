from domain_model.entities.group_setting import GroupSetting
from repositories import group_setting_repository
from use_cases.web.update_config_for_web_use_case import UpdateConfigForWebUseCase

from _web_test_utils import create_app, request_context


def test_execute_updates_group_setting_fields():
    # 目的: test_execute_updates_group_setting_fields の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.rate が 3 である / updated.rounding_method が 2 である
    # reply_service: なし
    # DB操作: created = group_setting_repository.create(GroupSetting(line_group_id="G1", rate=1)); updated = group_setting_repository.find({"_id": created._id})[0]
    # Arrange
    created = group_setting_repository.create(GroupSetting(line_group_id="G1", rate=1))
    app = create_app()
    use_case = UpdateConfigForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_group_id": "G1",
        "rate": "3",
        "rounding_method": "2",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = group_setting_repository.find({"_id": created._id})[0]
    assert updated.rate == 3
    assert updated.rounding_method == 2


def test_execute_with_no_fields_does_nothing():
    # 目的: test_execute_with_no_fields_does_nothing の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.rate が 1 である
    # reply_service: なし
    # DB操作: created = group_setting_repository.create(GroupSetting(line_group_id="G1", rate=1)); updated = group_setting_repository.find({"_id": created._id})[0]
    # Arrange
    created = group_setting_repository.create(GroupSetting(line_group_id="G1", rate=1))
    app = create_app()
    use_case = UpdateConfigForWebUseCase()

    form = {
        "_id": str(created._id),
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = group_setting_repository.find({"_id": created._id})[0]
    assert updated.rate == 1
