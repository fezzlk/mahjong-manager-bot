from bson.objectid import ObjectId
from dummies import generate_dummy_match_list

from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.match import Match, MatchStatus
from repositories import match_repository


def test_success():
    # Arrange
    dummy_match = generate_dummy_match_list()[0]

    # Act
    result = match_repository.create(
        dummy_match,
    )

    # Assert
    assert isinstance(result, Match)
    assert type(result._id) is ObjectId
    assert result.line_group_id == dummy_match.line_group_id
    assert result.is_deleted == dummy_match.is_deleted

    record_on_db = match_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0]._id == dummy_match._id
    assert record_on_db[0].line_group_id == dummy_match.line_group_id
    assert record_on_db[0].is_deleted == dummy_match.is_deleted
    assert record_on_db[0].sum_prices == {}
    assert record_on_db[0].sum_prices_with_chip == {}
    assert record_on_db[0].chip_prices == {}
    assert record_on_db[0].chip_scores == {}
    assert record_on_db[0].sum_scores == {}


def test_success_without_id():
    # Arrange
    dummy_match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    )

    # Act
    result = match_repository.create(
        dummy_match,
    )

    # Assert
    assert isinstance(result, Match)
    assert type(result._id) is ObjectId
    assert result.line_group_id == dummy_match.line_group_id
    assert result.is_deleted == dummy_match.is_deleted

    record_on_db = match_repository.find()
    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) is ObjectId
    assert record_on_db[0].line_group_id == dummy_match.line_group_id
    assert record_on_db[0].is_deleted == dummy_match.is_deleted
    assert record_on_db[0].sum_prices == {}
    assert record_on_db[0].sum_prices_with_chip == {}
    assert record_on_db[0].chip_prices == {}
    assert record_on_db[0].chip_scores == {}
    assert record_on_db[0].sum_scores == {}


def test_success_with_status_name_and_settings():
    # Arrange
    dummy_match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=MatchStatus.open.value,
        name="9/6",
        settings=EmbeddedGroupSettings(rate=5),
    )

    # Act
    match_repository.create(dummy_match)

    # Assert
    record_on_db = match_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].status == MatchStatus.open.value
    assert record_on_db[0].name == "9/6"
    assert record_on_db[0].settings == EmbeddedGroupSettings(rate=5)
