from tests.dummies import generate_dummy_room_list
from repositories import session_scope, room_repository
from domains.Room import Room


def test_hit_with_ids():
    # Arrange
    with session_scope() as session:
        dummy_rooms = generate_dummy_room_list()[:3]
        for dummy_room in dummy_rooms:
            room_repository.create(
                session,
                dummy_room,
            )
    target_rooms = generate_dummy_room_list()[1:3]
    ids = [target_room._id for target_room in target_rooms]

    # Act
    with session_scope() as session:
        result = room_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == len(target_rooms)
        for i in range(len(result)):
            assert isinstance(result[i], Room)
            assert result[i].line_room_id == target_rooms[i].line_room_id
            assert result[i].zoom_url == target_rooms[i].zoom_url
            assert result[i].mode == target_rooms[i].mode


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_rooms = generate_dummy_room_list()[:3]
        for dummy_room in dummy_rooms:
            room_repository.create(
                session,
                dummy_room,
            )
    target_rooms = generate_dummy_room_list()[3:6]
    ids = [target_room._id for target_room in target_rooms]

    # Act
    with session_scope() as session:
        result = room_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == 0
