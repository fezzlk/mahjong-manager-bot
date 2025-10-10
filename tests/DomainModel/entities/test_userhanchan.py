from datetime import datetime

from DomainModel.entities.UserHanchan import UserHanchan


def test_success():
    # Arrange

    # Act
    uh = UserHanchan(
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        hanchan_id=2,
        point=3,
        rank=4,
        yakuman_count=5,
        _id=1,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
    )

    # Assert
    assert uh._id == 1
    assert uh.line_user_id == "U0123456789abcdefghijklmnopqrstu2"
    assert uh.hanchan_id == 2
    assert uh.point == 3
    assert uh.rank == 4
    assert uh.yakuman_count == 5
    assert uh.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert uh.updated_at == datetime(2023, 1, 2, 3, 4, 5)


def test_success_default():
    # Arrange

    # Act
    uh = UserHanchan(
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        hanchan_id=2,
        point=3,
        rank=4,
    )

    # Assert
    assert uh._id is None
    assert uh.line_user_id == "U0123456789abcdefghijklmnopqrstu2"
    assert uh.hanchan_id == 2
    assert uh.point == 3
    assert uh.rank == 4
    assert uh.yakuman_count == 0
    assert uh.created_at.date() == datetime.now().date()
    assert uh.updated_at.date() == datetime.now().date()
