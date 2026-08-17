from bson.objectid import ObjectId

from domain_model.entities.match import Match
from domain_service import match_service
from repositories import match_repository


def test_updates_sum_scores():
    # Arrange
    match = Match(line_group_id="G0123456789abcdefghijklmnopqrstu1")
    match_repository.create(match)

    # Act
    match_service.update_sum_scores(match._id, {"U1": 100, "U2": -100})

    # Assert
    record = match_repository.find({"_id": match._id})[0]
    assert record.sum_scores == {"U1": 100, "U2": -100}


def test_does_not_touch_active_hanchan_id():
    """半荘確定処理中に別の対局が新たに開始されていても、sum_scoresの更新が
    その状態を上書きしないことを確認する(FEZ-49、Codex review指摘)
    """
    # Arrange
    newer_hanchan_id = ObjectId()
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=newer_hanchan_id,
    )
    match_repository.create(match)

    # Act
    match_service.update_sum_scores(match._id, {"U1": 100})

    # Assert
    record = match_repository.find({"_id": match._id})[0]
    assert record.active_hanchan_id == newer_hanchan_id
    assert record.sum_scores == {"U1": 100}
