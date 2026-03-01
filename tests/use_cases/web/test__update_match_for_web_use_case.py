from domain_model.entities.match import Match
from repositories import match_repository
from use_cases.web.update_match_for_web_use_case import UpdateMatchForWebUseCase

from _web_test_utils import create_app, request_context


def test_execute_updates_match_fields():
    # 目的: test_execute_updates_match_fields の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.line_group_id が "G2" である / updated.status が 1 である
    # reply_service: なし
    # DB操作: created = match_repository.create(Match(line_group_id="G1", status=2)); updated = match_repository.find({"_id": created._id})[0]
    # Arrange
    created = match_repository.create(Match(line_group_id="G1", status=2))
    app = create_app()
    use_case = UpdateMatchForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_group_id": "G2",
        "status": "1",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = match_repository.find({"_id": created._id})[0]
    assert updated.line_group_id == "G2"
    assert updated.status == 1


def test_execute_with_missing_status_keeps_existing():
    # 目的: test_execute_with_missing_status_keeps_existing の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.status が 2 である
    # reply_service: なし
    # DB操作: created = match_repository.create(Match(line_group_id="G1", status=2)); updated = match_repository.find({"_id": created._id})[0]
    # Arrange
    created = match_repository.create(Match(line_group_id="G1", status=2))
    app = create_app()
    use_case = UpdateMatchForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_group_id": "G1",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = match_repository.find({"_id": created._id})[0]
    assert updated.status == 2
