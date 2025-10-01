from DomainModel.entities.GroupSetting import GroupSetting
from repositories import group_setting_repository

before = GroupSetting(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    rate=3,
    ranking_prize=[20, 10, -10, -20],
    tip_rate=0,
    tobi_prize=10,
    num_of_players=4,
    rounding_method=0,
)

after = GroupSetting(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    rate=4,
    ranking_prize=[20, 10, -10, -20],
    tip_rate=0,
    tobi_prize=10,
    num_of_players=4,
    rounding_method=0,
)


def test_hit_1_record():
    # Arrange
    group_setting_repository.create(before)

    # Act
    result = group_setting_repository.update(
        query={"line_group_id": before.line_group_id},
        new_values={"rate": after.rate},
    )

    # Assert
    assert result == 1
    record_on_db = group_setting_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_group_id == after.line_group_id
    assert record_on_db[0].ranking_prize == after.ranking_prize
    assert record_on_db[0].tip_rate == after.tip_rate
    assert record_on_db[0].tobi_prize == after.tobi_prize
    assert record_on_db[0].num_of_players == after.num_of_players
    assert record_on_db[0].rounding_method == after.rounding_method


def test_hit_0_record():
    # Arrange

    # Act
    result = group_setting_repository.update(
        query={},
        new_values={"line_group_id": after.line_group_id},
    )

    # Assert
    assert result == 0
