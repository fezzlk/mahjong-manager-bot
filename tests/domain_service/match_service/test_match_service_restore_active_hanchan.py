from bson.objectid import ObjectId

from domain_model.entities.match import Match
from domain_service import match_service
from repositories import match_repository


def test_restores_when_still_cleared():
    # Arrange
    hanchan_id = ObjectId()
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=None,
    )
    match_repository.create(match)

    # Act
    match_service.restore_active_hanchan(match._id, hanchan_id)

    # Assert
    record = match_repository.find({"_id": match._id})[0]
    assert record.active_hanchan_id == hanchan_id


def test_does_not_overwrite_newer_active_hanchan():
    """復元しようとしている間に別の対局が新たに開始されていた場合、その状態を
    上書きしないことを確認する(FEZ-49、Codex review指摘)
    """
    # Arrange
    original_hanchan_id = ObjectId()
    newer_hanchan_id = ObjectId()
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=newer_hanchan_id,
    )
    match_repository.create(match)

    # Act: 復元対象のoriginal_hanchan_idはもはやactive_hanchan_idではない
    match_service.restore_active_hanchan(match._id, original_hanchan_id)

    # Assert: newer_hanchan_idのまま上書きされていない
    record = match_repository.find({"_id": match._id})[0]
    assert record.active_hanchan_id == newer_hanchan_id
