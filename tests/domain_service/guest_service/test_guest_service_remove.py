from domain_service import guest_service

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"


def test_remove_existing_returns_true():
    guest = guest_service.register_next(_LINE_GROUP_ID)

    result = guest_service.remove(_LINE_GROUP_ID, guest.guest_number)

    assert result is True
    assert guest_service.list_by_group(_LINE_GROUP_ID) == []


def test_remove_nonexistent_returns_false():
    result = guest_service.remove(_LINE_GROUP_ID, 999)

    assert result is False
