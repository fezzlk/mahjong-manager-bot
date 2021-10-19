from tests.dummies import generate_dummy_room_list
from db_setting import Session
from repositories import session_scope, room_repository
from domains.Room import Room

session = Session()


def test_hit_1_record():
    # Arrange
    dummy_rooms = generate_dummy_room_list()[:3]
    with session_scope() as session:
        for dummy_room in dummy_rooms:
            room_repository.create(
                session,
                dummy_room,
            )
    target_room = dummy_rooms[0]
    target_line_room_id = target_room.line_room_id

    # Act
    with session_scope() as session:
        result = room_repository.find_one_by_room_id(
            session,
            target_line_room_id,
        )

    # Assert
        assert isinstance(result, Room)
        assert result.line_room_id == target_room.line_room_id
        assert result.zoom_url == target_room.zoom_url
        assert result.mode == target_room.mode


def test_hit_0_record():
    # Arrange
    dummy_rooms = generate_dummy_room_list()[1:3]
    with session_scope() as session:
        for dummy_room in dummy_rooms:
            room_repository.create(
                session,
                dummy_room,
            )
    target_line_room_id = generate_dummy_room_list()[0].line_room_id

    # Act
    with session_scope() as session:
        result = room_repository.find_one_by_room_id(
            session,
            room_id=target_line_room_id,
        )

    # Assert
        assert result is None
