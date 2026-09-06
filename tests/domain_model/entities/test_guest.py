from datetime import datetime

from domain_model.entities.guest import Guest


def test_success():
    # Act
    guest = Guest(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        guest_number=3,
        is_deleted=True,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
        _id=1,
    )

    # Assert
    assert guest._id == 1
    assert guest.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert guest.guest_number == 3
    assert guest.is_deleted
    assert guest.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert guest.updated_at == datetime(2023, 1, 2, 3, 4, 5)


def test_success_default():
    # Act
    guest = Guest(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        guest_number=1,
    )

    # Assert
    assert guest._id is None
    assert not guest.is_deleted
    assert guest.created_at.date() == datetime.now().date()
    assert guest.updated_at.date() == datetime.now().date()
