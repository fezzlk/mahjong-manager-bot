from datetime import datetime

from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.match import Match, MatchStatus


def test_success():
    # Arrange

    # Act
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        is_deleted=True,
        status=MatchStatus.settled.value,
        name="9/6 (2)",
        settings=EmbeddedGroupSettings(rate=1),
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
        chip_prices={"a": 1},
        chip_scores={"a": 2},
        sum_prices={"a": 3},
        sum_prices_with_chip={"a": 4},
        sum_scores={"a": 5},
        active_hanchan_id=3,
        original_id=2,
        _id=1,
    )

    # Assert
    assert match._id == 1
    assert match.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert match.is_deleted
    assert match.status == MatchStatus.settled.value
    assert match.name == "9/6 (2)"
    assert match.settings == EmbeddedGroupSettings(rate=1)
    assert match.chip_prices == {"a": 1}
    assert match.chip_scores == {"a": 2}
    assert match.sum_prices == {"a": 3}
    assert match.sum_prices_with_chip == {"a": 4}
    assert match.sum_scores == {"a": 5}
    assert match.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert match.updated_at == datetime(2023, 1, 2, 3, 4, 5)
    assert match.active_hanchan_id == 3
    assert match.original_id == 2


def test_success_default():
    # Arrange

    # Act
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
    )

    # Assert
    assert match._id is None
    assert match.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert not match.is_deleted
    assert match.status == MatchStatus.open.value
    assert match.name is None
    assert match.settings is None
    assert match.chip_prices == {}
    assert match.chip_scores == {}
    assert match.sum_prices == {}
    assert match.sum_prices_with_chip == {}
    assert match.sum_scores == {}
    assert match.created_at.date() == datetime.now().date()
    assert match.updated_at.date() == datetime.now().date()
    assert match.active_hanchan_id is None
    assert match.original_id is None
