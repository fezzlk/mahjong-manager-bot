from datetime import datetime

from DomainModel.entities.WebUser import WebUser


def test_success():
    # Arrange

    # Act
    webuser = WebUser(
        user_code="code",
        name="name",
        email="email",
        _id=1,
        linked_line_user_id="U0123456789abcdefghijklmnopqrstu2",
        is_approved_line_user=True,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
    )

    # Assert
    assert webuser._id == 1
    assert webuser.user_code == "code"
    assert webuser.linked_line_user_id == "U0123456789abcdefghijklmnopqrstu2"
    assert webuser.name == "name"
    assert webuser.email == "email"
    assert webuser.is_approved_line_user is True
    assert webuser.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert webuser.updated_at == datetime(2023, 1, 2, 3, 4, 5)


def test_success_default():
    # Arrange

    # Act
    webuser = WebUser(
        user_code="code",
    )

    # Assert
    assert webuser._id is None
    assert webuser.user_code == "code"
    assert webuser.linked_line_user_id is None
    assert webuser.name is None
    assert webuser.email is None
    assert webuser.is_approved_line_user is False
    assert webuser.created_at.date() == datetime.now().date()
    assert webuser.updated_at.date() == datetime.now().date()
