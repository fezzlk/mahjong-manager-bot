from datetime import datetime

from DomainModel.entities.UserGroup import UserGroup


def test_success():
    # Arrange

    # Act
    ug = UserGroup(
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        _id=1,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
    )

    # Assert
    assert ug._id == 1
    assert ug.line_user_id == "U0123456789abcdefghijklmnopqrstu2"
    assert ug.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert ug.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert ug.updated_at == datetime(2023, 1, 2, 3, 4, 5)


def test_success_default():
    # Arrange

    # Act
    ug = UserGroup(
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
    )

    # Assert
    assert ug._id is None
    assert ug.line_user_id == "U0123456789abcdefghijklmnopqrstu2"
    assert ug.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert ug.created_at.date() == datetime.now().date()
    assert ug.updated_at.date() == datetime.now().date()
