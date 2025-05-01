from datetime import datetime

from DomainModel.entities.Match import Match


def test_success():
    # Arrange

    # Act
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        status=0,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
        tip_prices={"a":1},
        tip_scores={"a":2},
        sum_prices={"a":3},
        sum_prices_with_tip={"a": 4},
        sum_scores={"a":5},
        active_hanchan_id=3,
        original_id=2,
        _id=1,
    )

    # Assert
    assert match._id == 1
    assert match.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert match.status == 0
    assert match.tip_prices == {"a":1}
    assert match.tip_scores == {"a":2}
    assert match.sum_prices == {"a":3}
    assert match.sum_prices_with_tip == {"a":4}
    assert match.sum_scores == {"a":5}
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
    assert match.status == 2
    assert match.tip_prices == {}
    assert match.tip_scores == {}
    assert match.sum_prices == {}
    assert match.sum_prices_with_tip == {}
    assert match.sum_scores == {}
    assert match.created_at.date() == datetime.now().date()
    assert match.updated_at.date() == datetime.now().date()
    assert match.active_hanchan_id is None
    assert match.original_id is None
