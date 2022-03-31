import pytest
from DomainModel.entities.Match import Match
from DomainModel.entities.Hanchan import Hanchan
from DomainService.HanchanService import HanchanService
from repositories import session_scope, hanchan_repository, match_repository

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[],
        users=[],
        status=1,
        _id=1,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        hanchan_ids=[],
        users=[],
        status=1,
        _id=2,
    ),
]

dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={},
        converted_scores={},
        match_id=1,
        status=1,
        _id=1,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={},
        converted_scores={},
        match_id=1,
        status=2,
        _id=2,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={},
        converted_scores={},
        match_id=1,
        status=0,
        _id=3,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        raw_scores={},
        converted_scores={},
        match_id=2,
        status=0,
        _id=4,
    ),
]


def test_success():
    # Arrange
    hanchan_service = HanchanService()
    target_hanchan = dummy_hanchans[0]
    with session_scope() as session:
        for dummy_match in dummy_matches[0:2]:
            match_repository.create(session, dummy_match)

        for dummy_hanchan in dummy_hanchans[0:3]:
            hanchan_repository.create(session, dummy_hanchan)

    # Act
    result: Hanchan = hanchan_service.disable(
        line_group_id=target_hanchan.line_group_id,
    )

    # Assert
    assert result._id == target_hanchan._id
    assert result.line_group_id == target_hanchan.line_group_id
    assert result.status == 0


def test_fail_invalid_line_group_id():
    with pytest.raises(ValueError):
        # Arrange
        hanchan_service = HanchanService()
        target_hanchan = dummy_hanchans[3]
        with session_scope() as session:
            for dummy_match in dummy_matches[0:2]:
                match_repository.create(session, dummy_match)

            for dummy_hanchan in dummy_hanchans[0:3]:
                hanchan_repository.create(session, dummy_hanchan)

        # Act
        hanchan_service.disable(
            line_group_id=target_hanchan.line_group_id,
        )

        # Assert


def test_fail_not_active():
    with pytest.raises(ValueError):
        # Arrange
        hanchan_service = HanchanService()
        target_hanchan = dummy_hanchans[1]
        with session_scope() as session:
            for dummy_match in dummy_matches[0:2]:
                match_repository.create(session, dummy_match)

            for dummy_hanchan in dummy_hanchans[1:3]:
                hanchan_repository.create(session, dummy_hanchan)

        # Act
        hanchan_service.disable(
            line_group_id=target_hanchan.line_group_id,
        )

        # Assert
