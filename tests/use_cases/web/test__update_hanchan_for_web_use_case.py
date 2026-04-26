from _web_test_utils import create_app, request_context

from domain_model.entities.hanchan import Hanchan
from repositories import hanchan_repository
from use_cases.web.update_hanchan_for_web_use_case import UpdateHanchanForWebUseCase


def test_execute_updates_hanchan_fields():
    # 目的: test_execute_updates_hanchan_fields の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.line_group_id が "G2" である / updated.raw_scores が {"U1": 25000} である
    # reply_service: なし
    # DB操作: created = hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1)); updated = hanchan_repository.find({"_id": created._id})[0]
    # Arrange
    created = hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1))
    app = create_app()
    use_case = UpdateHanchanForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_group_id": "G2",
        "raw_scores": "{'U1': 25000}",
        "converted_scores": "{'U1': 10}",
        "match_id": str(created.match_id),
        "is_deleted": "False",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = hanchan_repository.find({"_id": created._id})[0]
    assert updated.line_group_id == "G2"
    assert updated.raw_scores == {"U1": 25000}


def test_execute_with_missing_scores_uses_empty():
    # 目的: test_execute_with_missing_scores_uses_empty の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: updated.status が 2 である
    # reply_service: なし
    # DB操作: created = hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1)); updated = hanchan_repository.find({"_id": created._id})[0]
    # Arrange
    created = hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1))
    app = create_app()
    use_case = UpdateHanchanForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_group_id": "G1",
        "match_id": str(created.match_id),
        "is_deleted": "False",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = hanchan_repository.find({"_id": created._id})[0]
    assert not updated.is_deleted
