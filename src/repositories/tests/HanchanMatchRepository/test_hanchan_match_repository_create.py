# from DomainModel.entities.HanchanMatch import HanchanMatch
# from repositories import (
#     hanchan_repository,
#     match_repository,
#     hanchan_match_repository,
# )
# from bson.objectid import ObjectId
# from tests.dummies import (
#     generate_dummy_hanchan_list,
#     generate_dummy_match_list,
# )
# import pytest


# dummy_hanchan = generate_dummy_hanchan_list()[0]
# dummy_match = generate_dummy_match_list()[0]


# def test_success():
#     # Arrange
#     new_hanchan = hanchan_repository.create(
#         dummy_hanchan,
#     )
#     new_match = match_repository.create(
#         dummy_match,
#     )
#     dummy_hanchan_match = HanchanMatch(
#         hanchan_id=new_hanchan._id,
#         match_id=new_match._id,
#     )

#     # Act
#     result = hanchan_match_repository.create(
#         dummy_hanchan_match,
#     )

#     # Assert
#     assert isinstance(result, HanchanMatch)
#     assert type(result._id) == ObjectId
#     assert result.hanchan_id == dummy_hanchan_match.hanchan_id
#     assert result.match_id == dummy_hanchan_match.match_id

#     record_on_db = hanchan_match_repository.find()
#     assert len(record_on_db) == 1
#     assert type(record_on_db[0]._id) == ObjectId
#     assert record_on_db[0].hanchan_id == dummy_hanchan_match.hanchan_id
#     assert record_on_db[0].match_id == dummy_hanchan_match.match_id


# def test_error_duplicate_line_group_id():
#     with pytest.raises(Exception):
#         # Arrange
#         new_hanchan = hanchan_repository.create(
#             dummy_hanchan,
#         )
#         new_match = match_repository.create(
#             dummy_match,
#         )
#         dummy_hanchan_match = HanchanMatch(
#             hanchan_id=new_hanchan._id,
#             match_id=new_match._id,
#         )

#         hanchan_match_repository.create(
#             dummy_hanchan_match,
#         )

#         # Act
#         hanchan_match_repository.create(
#             dummy_hanchan_match,
#         )

#         # Assert
#         record_on_db = hanchan_match_repository.find()
#         assert len(record_on_db) == 1
