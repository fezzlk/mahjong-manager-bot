from application_models.page_contents import PageContents
from domain_model.entities.web_user import WebUser
from repositories import web_user_repository

from ._web_test_utils import create_app, request_context


def test_init_sets_login_user_from_session_id():
    # Arrange
    created = web_user_repository.create(WebUser(user_code="code", name="Alice", email="a@example.com"))
    app = create_app()

    # Act
    with request_context(app, session_data={"login_user_id": created._id}):
        page_contents = PageContents(session={"login_user_id": created._id}, request=None)

    # Assert
    assert page_contents.login_user is not None
    assert page_contents.login_user._id == created._id
