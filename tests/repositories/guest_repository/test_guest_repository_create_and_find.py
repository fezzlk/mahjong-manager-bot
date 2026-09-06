from bson.objectid import ObjectId

from domain_model.entities.guest import Guest
from repositories import guest_repository


def test_create_and_find():
    # Act
    result = guest_repository.create(
        Guest(line_group_id="G0123456789abcdefghijklmnopqrstu1", guest_number=1),
    )

    # Assert
    assert isinstance(result, Guest)
    assert type(result._id) is ObjectId

    records = guest_repository.find()
    assert len(records) == 1
    assert records[0].guest_number == 1
    assert not records[0].is_deleted


def test_find_excludes_deleted():
    guest_repository.create(
        Guest(line_group_id="G0123456789abcdefghijklmnopqrstu1", guest_number=1),
    )
    guest_repository.create(
        Guest(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            guest_number=2,
            is_deleted=True,
        ),
    )

    records = guest_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})

    assert len(records) == 1
    assert records[0].guest_number == 1
