from datetime import datetime

from DomainModel.entities.UserMatch import UserMatch


def test_success():
    # Arrange

    # Act
    um = UserMatch(
        user_id=2,
        match_id=3,
        _id=1,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
    )

    # Assert
    assert um._id == 1
    assert um.user_id == 2
    assert um.match_id == 3
    assert um.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert um.updated_at == datetime(2023, 1, 2, 3, 4, 5)


def test_success_default():
    # Arrange

    # Act
    um = UserMatch(
        user_id=2,
        match_id=3,
    )

    # Assert
    assert um._id is None
    assert um.user_id == 2
    assert um.match_id == 3
    assert um.created_at.date() == datetime.now().date()
    assert um.updated_at.date() == datetime.now().date()
