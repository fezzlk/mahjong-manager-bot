from DomainModel.entities.Match import Match
from tests.dummies import generate_dummy_match_list
from repositories import match_repository
from bson.objectid import ObjectId


def test_success():
    # Arrange
    dummy_match = generate_dummy_match_list()[0]

    # Act
    result = match_repository.create(
        dummy_match,
    )

    # Assert
    assert isinstance(result, Match)
    assert type(result._id) == ObjectId
    assert result.line_group_id == dummy_match.line_group_id
    assert result.status == dummy_match.status
    
    record_on_db = match_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0]._id == dummy_match._id
    assert record_on_db[0].line_group_id == dummy_match.line_group_id
    assert record_on_db[0].status == dummy_match.status


def test_success_without_id():
    # Arrange
    dummy_match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
    )

    # Act
    result = match_repository.create(
        dummy_match,
    )

    # Assert
    assert isinstance(result, Match)
    assert type(result._id) == ObjectId
    assert result.line_group_id == dummy_match.line_group_id
    assert result.status == dummy_match.status
    
    record_on_db = match_repository.find()
    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) == ObjectId
    assert record_on_db[0].line_group_id == dummy_match.line_group_id
    assert record_on_db[0].status == dummy_match.status
