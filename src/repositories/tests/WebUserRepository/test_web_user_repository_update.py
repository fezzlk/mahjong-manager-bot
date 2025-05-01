from datetime import datetime

from DomainModel.entities.WebUser import WebUser
from repositories import web_user_repository

before = WebUser(
    user_code="code",
    name="name1",
    email="email1",
    linked_line_user_id=None,
    is_approved_line_user=False,
    created_at=datetime(2022, 1, 1, 12, 0, 0),
    updated_at=datetime(2022, 1, 1, 12, 0, 0),
)
after = WebUser(
    user_code="code",
    name="name2",
    email="email2",
    linked_line_user_id=None,
    is_approved_line_user=True,
    created_at=datetime(2022, 1, 1, 12, 0, 0),
    updated_at=datetime(2022, 1, 1, 12, 0, 0),
)


def test_hit_1_record():
    # Arrange
    web_user_repository.create(
        before,
    )

    # Act
    web_user_repository.update(
        query={"user_code": before.user_code},
        new_values={
            "name": after.name,
            "email": after.email,
            "is_approved_line_user": after.is_approved_line_user,
        },
    )

    # Assert
    result = web_user_repository.find()[0]
    assert isinstance(result, WebUser)
    assert result.user_code == after.user_code
    assert result.name == after.name
    assert result.email == after.email
    assert result.linked_line_user_id == after.linked_line_user_id
    assert result.is_approved_line_user == after.is_approved_line_user
