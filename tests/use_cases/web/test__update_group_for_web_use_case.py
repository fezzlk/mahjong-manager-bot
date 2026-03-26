from _web_test_utils import create_app, request_context

from domain_model.entities.group import Group
from repositories import group_repository
from use_cases.web.update_group_for_web_use_case import UpdateGroupForWebUseCase


def test_execute_updates_group_fields():
    # 目的: test_execute_updates_group_fields の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.line_group_id が "G2" である
    # reply_service: なし
    # DB操作: created = group_repository.create(Group(line_group_id="G1")); updated = group_repository.find({"_id": created._id})[0]
    # Arrange
    created = group_repository.create(Group(line_group_id="G1"))
    app = create_app()
    use_case = UpdateGroupForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_group_id": "G2",
        "mode": "GroupMode.wait",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = group_repository.find({"_id": created._id})[0]
    assert updated.line_group_id == "G2"


def test_execute_with_missing_mode_keeps_existing():
    # 目的: test_execute_with_missing_mode_keeps_existing の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.line_group_id が "G1" である
    # reply_service: なし
    # DB操作: created = group_repository.create(Group(line_group_id="G1")); updated = group_repository.find({"_id": created._id})[0]
    # Arrange
    created = group_repository.create(Group(line_group_id="G1"))
    app = create_app()
    use_case = UpdateGroupForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_group_id": "G1",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = group_repository.find({"_id": created._id})[0]
    assert updated.line_group_id == "G1"
