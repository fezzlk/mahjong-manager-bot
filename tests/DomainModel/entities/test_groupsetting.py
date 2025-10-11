from datetime import datetime

from DomainModel.entities.GroupSetting import GroupSetting


def test_success():
    # Arrange

    # Act
    setting = GroupSetting(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        rate=3,
        ranking_prize=[30,10,-10,-30],
        tip_rate=30,
        tobi_prize=10,
        num_of_players=3,
        rounding_method=2,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
        _id=1,
    )

    # Assert
    assert setting._id == 1
    assert setting.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert setting.rate == 3
    assert setting.ranking_prize == [30,10,-10,-30]
    assert setting.tobi_prize == 10
    assert setting.num_of_players == 3
    assert setting.rounding_method ==2
    assert setting.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert setting.updated_at == datetime(2023, 1, 2, 3, 4, 5)


def test_success_default():
    # Arrange

    # Act
    setting = GroupSetting(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
    )

    # Assert
    assert setting._id is None
    assert setting.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert setting.rate == 0
    assert setting.ranking_prize == [20,10,-10,-20]
    assert setting.tobi_prize == 10
    assert setting.num_of_players == 4
    assert setting.rounding_method == 1
    assert setting.created_at.date() == datetime.now().date()
    assert setting.updated_at.date() == datetime.now().date()
