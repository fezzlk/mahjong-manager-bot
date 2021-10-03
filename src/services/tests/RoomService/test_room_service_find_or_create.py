from services.RoomService import RoomService
from repositories import session_scope, room_repository
from tests.dummies import generate_dummy_room_list
from domains.Room import Room


def test_create_new_user():
    # Arrange
    room_service = RoomService()
    dummy_room = generate_dummy_room_list()[0]

    # Act
    result = room_service.find_or_create(dummy_room.line_room_id)

    # Assert
    assert isinstance(result, Room)
    assert result.line_room_id == dummy_room.line_room_id


def test_find_exist_room():
    # Arrange
    room_service = RoomService()
    dummy_room = generate_dummy_room_list()[0]
    with session_scope() as session:
        room_repository.create(session, dummy_room)

    # Act
    result = room_service.find_or_create(dummy_room.line_room_id)

    # Assert
    assert isinstance(result, Room)
    assert result.line_room_id == dummy_room.line_room_id
    with session_scope() as session:
        records = room_repository.find_all(session)
        assert len(records) == 1
