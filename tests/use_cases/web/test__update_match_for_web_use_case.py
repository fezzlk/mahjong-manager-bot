from _web_test_utils import create_app, request_context

from domain_model.entities.match import Match
from repositories import match_repository
from use_cases.web.update_match_for_web_use_case import UpdateMatchForWebUseCase


def test_execute_updates_match_fields():
    # Arrange
    created = match_repository.create(Match(line_group_id="G1"))
    app = create_app()
    use_case = UpdateMatchForWebUseCase()

    form = {
        "_id": str(created._id),
        "line_group_id": "G2",
        "is_deleted": "false",
    }

    # Act
    with request_context(app, form_data=form):
        use_case.execute()

    # Assert
    updated = match_repository.find({"_id": created._id})[0]
    assert updated.line_group_id == "G2"
    assert not updated.is_deleted


def test_execute_with_missing_is_deleted_keeps_existing():
    # Arrange
    created = match_repository.create(Match(line_group_id="G1"))
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
    assert not updated.is_deleted
