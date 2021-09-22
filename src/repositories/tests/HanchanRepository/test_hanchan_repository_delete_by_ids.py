# from tests.dummies import generate_dummy_room_list
# from db_setting import Session
# from repositories import session_scope
# from repositories.room_repository import RoomRepository
# from domains.room import Room

# session = Session()


# def test_hit_with_ids():
#     # Arrange
#     dummy_rooms = generate_dummy_room_list()[:3]
#     with session_scope() as session:
#         for dummy_room in dummy_rooms:
#             RoomRepository.create(
#                 session,
#                 dummy_room,
#             )
#     other_rooms = dummy_rooms[:1]
#     target_rooms = dummy_rooms[1:3]
#     ids = [target_room._id for target_room in target_rooms]

#     # Act
#     with session_scope() as session:
#         RoomRepository.delete_by_ids(
#             session,
#             ids,
#         )

#     # Assert
#     with session_scope() as session:
#         result = RoomRepository.find_all(
#             session,
#         )
#         assert len(result) == len(other_rooms)
#         for i in range(len(result)):
#             assert isinstance(result[i], Room)
#             assert result[i].line_room_id == other_rooms[i].line_room_id
#             assert result[i].zoom_url == other_rooms[i].zoom_url
#             assert result[i].mode == other_rooms[i].mode


# def test_hit_with_an_id_as_not_list():
#     # Arrange
#     dummy_rooms = generate_dummy_room_list()[:3]
#     with session_scope() as session:
#         for dummy_room in dummy_rooms:
#             RoomRepository.create(
#                 session,
#                 dummy_room,
#             )
#     other_rooms = dummy_rooms[:2]
#     target_room = dummy_rooms[2]
#     target_room_id = target_room._id

#     # Act
#     with session_scope() as session:
#         result = RoomRepository.delete_by_ids(
#             session,
#             target_room_id,
#         )

#     # Assert
#     with session_scope() as session:
#         result = RoomRepository.find_all(
#             session,
#         )
#         assert len(result) == len(other_rooms)
#         for i in range(len(result)):
#             assert isinstance(result[i], Room)
#             assert result[i].line_room_id == other_rooms[i].line_room_id
#             assert result[i].zoom_url == other_rooms[i].zoom_url
#             assert result[i].mode == other_rooms[i].mode


# def test_hit_0_record():
#     # Arrange
#     with session_scope() as session:
#         dummy_rooms = generate_dummy_room_list()[:3]
#         for dummy_room in dummy_rooms:
#             RoomRepository.create(
#                 session,
#                 dummy_room,
#             )
#     target_rooms = generate_dummy_room_list()[3:6]
#     ids = [target_room._id for target_room in target_rooms]

#     # Act
#     with session_scope() as session:
#         result = RoomRepository.delete_by_ids(
#             session,
#             ids,
#         )

#     # Assert
#     with session_scope() as session:
#         result = RoomRepository.find_all(
#             session,
#         )
#         assert len(result) == len(dummy_rooms)
#         for i in range(len(result)):
#             assert isinstance(result[i], Room)
#             assert result[i].line_room_id == dummy_rooms[i].line_room_id
#             assert result[i].zoom_url == dummy_rooms[i].zoom_url
#             assert result[i].mode == dummy_rooms[i].mode