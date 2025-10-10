from repositories import group_setting_repository
from dummies import generate_dummy_group_setting_list


def test_hit_with_ids():
    # Arrange
    dummy_group_settings = generate_dummy_group_setting_list()[:3]
    for dummy_group_setting in dummy_group_settings:
        group_setting_repository.create(
            dummy_group_setting,
        )
    other_groups = dummy_group_settings[:1]
    target_groups = dummy_group_settings[1:3]
    ids = [target_group._id for target_group in target_groups]

    # Act
    result = group_setting_repository.delete(
        query={"_id": {"$in": ids}},
    )

    # Assert
    assert result == len(target_groups)
    record_on_db = group_setting_repository.find()
    assert len(record_on_db) == len(other_groups)
    for i in range(len(record_on_db)):
        assert record_on_db[i].line_group_id == other_groups[i].line_group_id
        assert record_on_db[i].ranking_prize == other_groups[i].ranking_prize
        assert record_on_db[i].tip_rate == other_groups[i].tip_rate
        assert record_on_db[i].tobi_prize == other_groups[i].tobi_prize
        assert record_on_db[i].num_of_players == other_groups[i].num_of_players
        assert record_on_db[i].rounding_method == other_groups[i].rounding_method


def test_hit_0_record():
    # Arrange
    dummy_group_settings = generate_dummy_group_setting_list()[:3]
    for dummy_group_setting in dummy_group_settings:
        group_setting_repository.create(
            dummy_group_setting,
        )
    target_groups = generate_dummy_group_setting_list()[3:6]
    ids = [target_group._id for target_group in target_groups]

    # Act
    result = group_setting_repository.delete(
        query={"_id": {"$in": ids}},
    )

    # Assert
    assert result == 0
    record_on_db = group_setting_repository.find()
    assert len(record_on_db) == len(dummy_group_settings)
    for i in range(len(record_on_db)):
        assert record_on_db[i].line_group_id == dummy_group_settings[i].line_group_id
        assert record_on_db[i].ranking_prize == dummy_group_settings[i].ranking_prize
        assert record_on_db[i].tip_rate == dummy_group_settings[i].tip_rate
        assert record_on_db[i].tobi_prize == dummy_group_settings[i].tobi_prize
        assert record_on_db[i].num_of_players == dummy_group_settings[i].num_of_players
        assert record_on_db[i].rounding_method == dummy_group_settings[i].rounding_method
