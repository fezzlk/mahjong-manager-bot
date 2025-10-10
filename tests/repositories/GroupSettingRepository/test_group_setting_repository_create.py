import pytest
from bson.objectid import ObjectId

from DomainModel.entities.GroupSetting import GroupSetting
from repositories import group_setting_repository
from tests.dummies import generate_dummy_group_setting_list


def test_success():
    # Arrange
    dummy_group_setting = generate_dummy_group_setting_list()[0]

    # Act
    result = group_setting_repository.create(
        dummy_group_setting,
    )

    # Assert
    assert isinstance(result, GroupSetting)
    assert result.line_group_id == dummy_group_setting.line_group_id
    assert result.ranking_prize == dummy_group_setting.ranking_prize
    assert result.tip_rate == dummy_group_setting.tip_rate
    assert result.tobi_prize == dummy_group_setting.tobi_prize
    assert result.num_of_players == dummy_group_setting.num_of_players
    assert result.rounding_method == dummy_group_setting.rounding_method

    record_on_db = group_setting_repository.find()

    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) is ObjectId
    assert record_on_db[0].line_group_id == dummy_group_setting.line_group_id
    assert record_on_db[0].ranking_prize == dummy_group_setting.ranking_prize
    assert record_on_db[0].tip_rate == dummy_group_setting.tip_rate
    assert record_on_db[0].tobi_prize == dummy_group_setting.tobi_prize
    assert record_on_db[0].num_of_players == dummy_group_setting.num_of_players
    assert record_on_db[0].rounding_method == dummy_group_setting.rounding_method


def test_success_with_id():
    # Arrange
    dummy_group_setting = GroupSetting(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        rate=3,
        ranking_prize=[20, 10, -10, -20],
        tip_rate=0,
        tobi_prize=10,
        num_of_players=4,
        rounding_method=0,
        _id=ObjectId("644c838186bbd9e20a91b783"),
    )

    # Act
    result = group_setting_repository.create(
        dummy_group_setting,
    )

    # Assert
    assert isinstance(result, GroupSetting)
    assert result._id == dummy_group_setting._id
    assert result.line_group_id == dummy_group_setting.line_group_id
    assert result.ranking_prize == dummy_group_setting.ranking_prize
    assert result.tip_rate == dummy_group_setting.tip_rate
    assert result.tobi_prize == dummy_group_setting.tobi_prize
    assert result.num_of_players == dummy_group_setting.num_of_players
    assert result.rounding_method == dummy_group_setting.rounding_method

    record_on_db = group_setting_repository.find()

    assert len(record_on_db) == 1
    assert record_on_db[0]._id == dummy_group_setting._id
    assert record_on_db[0].line_group_id == dummy_group_setting.line_group_id
    assert record_on_db[0].ranking_prize == dummy_group_setting.ranking_prize
    assert record_on_db[0].tip_rate == dummy_group_setting.tip_rate
    assert record_on_db[0].tobi_prize == dummy_group_setting.tobi_prize
    assert record_on_db[0].num_of_players == dummy_group_setting.num_of_players
    assert record_on_db[0].rounding_method == dummy_group_setting.rounding_method


def test_error_duplicate_line_group_id():
    with pytest.raises(Exception):
        # Arrange
        dummy_group_settings = [
            GroupSetting(
                line_group_id="G0123456789abcdefghijklmnopqrstu1",
                rate=3,
                ranking_prize=[20, 10, -10, -20],
                tip_rate=0,
                tobi_prize=10,
                num_of_players=4,
                rounding_method=0,
            ),
            GroupSetting(
                line_group_id="G0123456789abcdefghijklmnopqrstu1",
                rate=3,
                ranking_prize=[30, 10, -10, -30],
                tip_rate=0,
                tobi_prize=10,
                num_of_players=4,
                rounding_method=0,
            ),
        ]
        group_setting_repository.create(
            dummy_group_settings[0],
        )

        # Act
        group_setting_repository.create(
            dummy_group_settings[1],
        )

    # Assert
    record_on_db = group_setting_repository.find()
    assert len(record_on_db) == 1
