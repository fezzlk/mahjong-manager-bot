# from tests.dummies import generate_dummy_room_list
# from db_setting import Session
# from repositories import session_scope
# from repositories.room_repository import RoomRepository
# from domains.room import Room

# session = Session()


# def test_success_find_records():
#     # Arrange
#     with session_scope() as session:
#         dummy_rooms = generate_dummy_room_list()
#         for dummy_room in dummy_rooms:
#             RoomRepository.create(
#                 session,
#                 dummy_room,
#             )

#     # Act
#     with session_scope() as session:
#         result = RoomRepository.find_all(
#             session,
#         )

#     # Assert
#         assert len(result) == len(dummy_rooms)
#         for i in range(len(result)):
#             assert isinstance(result[i], Room)
#             assert result[i].line_room_id == dummy_rooms[i].line_room_id
#             assert result[i].zoom_url == dummy_rooms[i].zoom_url
#             assert result[i].mode == dummy_rooms[i].mode


# def test_success_find_0_record():
#     # Arrange
#     # Do nothing

#     # Act
#     with session_scope() as session:
#         result = RoomRepository.find_all(
#             session,
#         )

#     # Assert
#         assert len(result) == 0
