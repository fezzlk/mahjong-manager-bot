# from DomainModel.entities.Hanchan import Hanchan
# from DomainModel.entities.Match import Match
# from DomainModel.entities.HanchanMatch import HanchanMatch
# from repositories import (
#     hanchan_repository,
#     match_repository,
#     hanchan_match_repository,
# )
# from typing import List
# from pymongo import DESCENDING
# from tests.dummies import (
#     generate_dummy_hanchan_list,
#     generate_dummy_match_list,
# )

# dummy_hanchans = generate_dummy_hanchan_list()
# dummy_matches = generate_dummy_match_list()


# def test_success():
#     # Arrange
#     hanchans: List[Hanchan] = []
#     matches: List[Match] = []
#     for dummy_hanchan in dummy_hanchans:
#         hanchans.append(
#             hanchan_repository.create(dummy_hanchan)
#         )
#     for dummy_match in dummy_matches:
#         matches.append(
#             match_repository.create(dummy_match)
#         )
#     dummy_hanchan_matches = [
#         HanchanMatch(
#             hanchan_id=hanchans[0]._id,
#             match_id=matches[0]._id,
#         ),
#         HanchanMatch(
#             hanchan_id=hanchans[1]._id,
#             match_id=matches[0]._id,
#         ),
#         HanchanMatch(
#             hanchan_id=hanchans[0]._id,
#             match_id=matches[1]._id,
#         ),
#     ]
#     for dummy_hanchan_match in dummy_hanchan_matches:
#         hanchan_match_repository.create(
#             dummy_hanchan_match,
#         )

#     # Act
#     result = hanchan_match_repository.find()

#     # Assert
#     assert len(result) == len(dummy_hanchan_matches)
#     for i in range(len(result)):
#         assert result[i].hanchan_id == dummy_hanchan_matches[i].hanchan_id
#         assert result[i].match_id == dummy_hanchan_matches[i].match_id


# def test_success_with_filter():
#     # Arrange
#     hanchans: List[Hanchan] = []
#     matches: List[Match] = []
#     for dummy_hanchan in dummy_hanchans:
#         hanchans.append(
#             hanchan_repository.create(dummy_hanchan)
#         )
#     for dummy_match in dummy_matches:
#         matches.append(
#             match_repository.create(dummy_match)
#         )
#     dummy_hanchan_matches = [
#         HanchanMatch(
#             hanchan_id=hanchans[0]._id,
#             match_id=matches[0]._id,
#         ),
#         HanchanMatch(
#             hanchan_id=hanchans[1]._id,
#             match_id=matches[0]._id,
#         ),
#         HanchanMatch(
#             hanchan_id=hanchans[0]._id,
#             match_id=matches[1]._id,
#         ),
#     ]
#     for dummy_hanchan_match in dummy_hanchan_matches:
#         hanchan_match_repository.create(
#             dummy_hanchan_match,
#         )
#     target = dummy_hanchan_matches[0]

#     # Act
#     result = hanchan_match_repository.find(
#         query={
#             'hanchan_id': target.hanchan_id,
#             'match_id': target.match_id,
#         },
#     )

#     # Assert
#     assert result[0].hanchan_id == target.hanchan_id
#     assert result[0].match_id == target.match_id


# def test_success_with_sort():
#     # Arrange
#     hanchans: List[Hanchan] = []
#     matches: List[Match] = []
#     for dummy_hanchan in dummy_hanchans:
#         hanchans.append(
#             hanchan_repository.create(dummy_hanchan)
#         )
#     for dummy_match in dummy_matches:
#         matches.append(
#             match_repository.create(dummy_match)
#         )
#     dummy_hanchan_matches = [
#         HanchanMatch(
#             hanchan_id=hanchans[0]._id,
#             match_id=matches[0]._id,
#         ),
#         HanchanMatch(
#             hanchan_id=hanchans[1]._id,
#             match_id=matches[0]._id,
#         ),
#         HanchanMatch(
#             hanchan_id=hanchans[0]._id,
#             match_id=matches[1]._id,
#         ),
#     ]
#     for dummy_hanchan_match in dummy_hanchan_matches:
#         hanchan_match_repository.create(
#             dummy_hanchan_match,
#         )

#     # Act
#     result = hanchan_match_repository.find(
#         query={
#             'hanchan_id': dummy_hanchan_matches[0].hanchan_id,
#         },
#         sort=[('match_id', DESCENDING)]
#     )
    
#     # Assert
#     expected = [
#         HanchanMatch(
#             hanchan_id=hanchans[0]._id,
#             match_id=matches[1]._id,
#         ),
#         HanchanMatch(
#             hanchan_id=hanchans[0]._id,
#             match_id=matches[0]._id,
#         ),
#     ]
#     assert len(result) == len(expected)
#     for i in range(len(result)):
#         assert result[i].hanchan_id == expected[i].hanchan_id
#         assert result[i].match_id == expected[i].match_id
