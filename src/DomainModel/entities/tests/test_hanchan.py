from datetime import datetime

from DomainModel.entities.Hanchan import Hanchan


def test_success():
    # Arrange

    # Act
    hanchan = Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        match_id=1,
        status=0,
        raw_scores={"a": 20000},
        converted_scores={"a": 20},
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
        original_id=2,
        _id=3,
    )

    # Assert
    assert hanchan._id == 3
    assert hanchan.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert hanchan.match_id == 1
    assert hanchan.status == 0
    assert hanchan.raw_scores == {"a": 20000}
    assert hanchan.converted_scores == {"a": 20}
    assert hanchan.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert hanchan.updated_at == datetime(2023, 1, 2, 3, 4, 5)
    assert hanchan.original_id == 2


def test_success_default():
    # Arrange

    # Act
    hanchan = Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        match_id=1,
    )

    # Assert
    assert hanchan._id is None
    assert hanchan.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert hanchan.match_id == 1
    assert hanchan.status == 2
    assert hanchan.raw_scores == {}
    assert hanchan.converted_scores == {}
    assert hanchan.created_at.date() == datetime.now().date()
    assert hanchan.updated_at.date() == datetime.now().date()
    assert hanchan.original_id is None
