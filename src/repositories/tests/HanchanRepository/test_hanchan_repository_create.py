from DomainModel.entities.Hanchan import Hanchan
from tests.dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)
from repositories import hanchan_repository, match_repository
from bson.objectid import ObjectId


def test_success():
    # Arrange
    dummy_hanchan = generate_dummy_hanchan_list()[0]
    dummy_match = generate_dummy_match_list()[0]
    match_repository.create(
        dummy_match,
    )

    # Act
    result = hanchan_repository.create(
        dummy_hanchan,
    )

    # Assert
    assert isinstance(result, Hanchan)
    assert type(result._id) == ObjectId
    assert result.line_group_id == dummy_hanchan.line_group_id
    assert result.raw_scores == dummy_hanchan.raw_scores
    assert result.converted_scores == dummy_hanchan.converted_scores
    assert result.match_id == dummy_hanchan.match_id
    assert result.status == dummy_hanchan.status

    record_on_db = hanchan_repository.find()
    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) == ObjectId
    assert record_on_db[0].line_group_id == dummy_hanchan.line_group_id
    assert record_on_db[0].raw_scores == dummy_hanchan.raw_scores
    assert record_on_db[0].converted_scores == dummy_hanchan.converted_scores
    assert record_on_db[0].match_id == dummy_hanchan.match_id
    assert record_on_db[0].status == dummy_hanchan.status
