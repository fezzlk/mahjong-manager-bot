from domain_service import guest_service

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"


def test_lists_in_ascending_order():
    guest_service.register_next(_LINE_GROUP_ID)
    guest_service.register_next(_LINE_GROUP_ID)
    guest_service.register_next(_LINE_GROUP_ID)

    guests = guest_service.list_by_group(_LINE_GROUP_ID)

    assert [g.guest_number for g in guests] == [1, 2, 3]


def test_excludes_removed_guests():
    guest_service.register_next(_LINE_GROUP_ID)
    second = guest_service.register_next(_LINE_GROUP_ID)
    guest_service.remove(_LINE_GROUP_ID, second.guest_number)

    guests = guest_service.list_by_group(_LINE_GROUP_ID)

    assert [g.guest_number for g in guests] == [1]


def test_scoped_by_line_group_id():
    guest_service.register_next(_LINE_GROUP_ID)
    guest_service.register_next("G0123456789abcdefghijklmnopqrstu2")

    guests = guest_service.list_by_group(_LINE_GROUP_ID)

    assert len(guests) == 1
