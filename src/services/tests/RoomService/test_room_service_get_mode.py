from services.RoomService import RoomService
from repositories import session_scope, room_repository
from tests.dummies import generate_dummy_room_list


def test_success():
    # Arrange
    room_service = RoomService()
    dummy_rooms = generate_dummy_room_list()[:3]
    dummy_room = dummy_rooms[0]
    with session_scope() as session:
        for record in dummy_rooms:
            room_repository.create(session, record)

    # Act
    result = room_service.get_mode(dummy_room.line_room_id)

    # Assert
    assert result == dummy_room.mode


def test_not_hit():
    # Arrange
    room_service = RoomService()
    dummy_rooms = generate_dummy_room_list()[:3]
    dummy_room = dummy_rooms[0]
    with session_scope() as session:
        for record in dummy_rooms[1:]:
            room_repository.create(session, record)

    # Act
    result = room_service.get_mode(dummy_room.line_room_id)

    # Assert
    assert result is None
