from bson.objectid import ObjectId
from dummies import generate_dummy_group_setting_list

from DomainModel.entities.GroupSetting import GroupSetting
from repositories import group_setting_repository


def test_success_find_records():
    # Arrange
    dummy_group_settings = generate_dummy_group_setting_list()[:2]
    for dummy_group_setting in dummy_group_settings:
        group_setting_repository.create(
            dummy_group_setting,
        )

    # Act
    result = group_setting_repository.find()

    # Assert
    assert len(result) == len(dummy_group_settings)
    for i in range(len(result)):
        assert isinstance(result[i], GroupSetting)
        assert type(result[i]._id) is ObjectId
        assert result[i].line_group_id == dummy_group_settings[i].line_group_id
        assert result[i].ranking_prize == dummy_group_settings[i].ranking_prize
        assert result[i].tip_rate == dummy_group_settings[i].tip_rate
        assert result[i].tobi_prize == dummy_group_settings[i].tobi_prize
        assert result[i].num_of_players == dummy_group_settings[i].num_of_players
        assert result[i].rounding_method == dummy_group_settings[i].rounding_method


def test_hit_0_record():
    # Arrange
    dummy_group_settings = generate_dummy_group_setting_list()[:1]
    for dummy_group_setting in dummy_group_settings:
        group_setting_repository.create(
            dummy_group_setting,
        )
    target_group = generate_dummy_group_setting_list()[1]

    # Act
    result = group_setting_repository.find(
        query={"line_group_id": target_group.line_group_id},
    )

    # Assert
    assert len(result) == 0


def test_hit_1_record():
    # Arrange
    dummy_group_settings = generate_dummy_group_setting_list()[:3]
    for dummy_group_setting in dummy_group_settings:
        group_setting_repository.create(
            dummy_group_setting,
        )
    target_group = dummy_group_settings[0]
    target_line_group_id = target_group.line_group_id

    # Act
    result = group_setting_repository.find(
        query={"line_group_id": target_line_group_id},
    )

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], GroupSetting)
    assert type(result[0]._id) is ObjectId
    assert result[0].line_group_id == target_group.line_group_id
    assert result[0].ranking_prize == target_group.ranking_prize
    assert result[0].tip_rate == target_group.tip_rate
    assert result[0].tobi_prize == target_group.tobi_prize
    assert result[0].num_of_players == target_group.num_of_players
    assert result[0].rounding_method == target_group.rounding_method
