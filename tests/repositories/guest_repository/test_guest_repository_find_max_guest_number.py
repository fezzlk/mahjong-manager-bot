from domain_model.entities.guest import Guest
from repositories import guest_repository

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"


def test_returns_none_when_no_guests():
    assert guest_repository.find_max_guest_number(_LINE_GROUP_ID) is None


def test_returns_max_including_deleted():
    """削除済みのゲストも含めて最大番号を返す(番号再利用防止)。"""
    guest_repository.create(Guest(line_group_id=_LINE_GROUP_ID, guest_number=1))
    guest_repository.create(
        Guest(line_group_id=_LINE_GROUP_ID, guest_number=2, is_deleted=True),
    )

    assert guest_repository.find_max_guest_number(_LINE_GROUP_ID) == 2


def test_scoped_by_line_group_id():
    guest_repository.create(Guest(line_group_id=_LINE_GROUP_ID, guest_number=5))
    guest_repository.create(
        Guest(line_group_id="G0123456789abcdefghijklmnopqrstu2", guest_number=9),
    )

    assert guest_repository.find_max_guest_number(_LINE_GROUP_ID) == 5
