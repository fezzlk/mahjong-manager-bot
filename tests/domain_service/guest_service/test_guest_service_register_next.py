from domain_service import guest_service

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"


def test_first_guest_is_number_one():
    guest = guest_service.register_next(_LINE_GROUP_ID)

    assert guest.guest_number == 1
    assert guest.line_group_id == _LINE_GROUP_ID


def test_increments_sequentially():
    guest_service.register_next(_LINE_GROUP_ID)
    second = guest_service.register_next(_LINE_GROUP_ID)

    assert second.guest_number == 2


def test_does_not_reuse_number_after_removal():
    """削除後も番号を再利用しない(将来のスコア記録との衝突防止)。"""
    first = guest_service.register_next(_LINE_GROUP_ID)
    guest_service.remove(_LINE_GROUP_ID, first.guest_number)

    next_guest = guest_service.register_next(_LINE_GROUP_ID)

    assert next_guest.guest_number == 2
