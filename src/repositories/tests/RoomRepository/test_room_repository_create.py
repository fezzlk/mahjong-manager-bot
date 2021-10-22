from tests.dummies import generate_dummy_room_list
from repositories import session_scope, room_repository


def test_success():
    # Arrange
    dummy_room = generate_dummy_room_list()[0]

    # Act
    with session_scope() as session:
        room_repository.create(
            session,
            dummy_room,
        )

    # Assert
    with session_scope() as session:
        result = room_repository.find_all(
            session,
        )
        assert len(result) == 1
        assert result[0].line_room_id == dummy_room.line_room_id
        assert result[0].zoom_url == dummy_room.zoom_url
        assert result[0].mode == dummy_room.mode
