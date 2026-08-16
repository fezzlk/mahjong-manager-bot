import threading

from bson.objectid import ObjectId

from domain_model.entities.match import Match
from domain_service import match_service
from repositories import match_repository


def test_clears_when_hanchan_matches():
    # Arrange
    hanchan_id = ObjectId()
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=hanchan_id,
    )
    match_repository.create(match)

    # Act
    result = match_service.try_clear_active_hanchan(match._id, hanchan_id)

    # Assert
    assert result is True
    record = match_repository.find({"_id": match._id})[0]
    assert record.active_hanchan_id is None


def test_returns_false_when_already_cleared():
    # Arrange
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=None,
    )
    match_repository.create(match)

    # Act
    result = match_service.try_clear_active_hanchan(match._id, ObjectId())

    # Assert
    assert result is False


def test_returns_false_when_hanchan_differs():
    # Arrange
    hanchan_id = ObjectId()
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=hanchan_id,
    )
    match_repository.create(match)

    # Act
    result = match_service.try_clear_active_hanchan(match._id, ObjectId())

    # Assert
    assert result is False
    record = match_repository.find({"_id": match._id})[0]
    assert record.active_hanchan_id == hanchan_id


def test_only_one_of_concurrent_claims_succeeds():
    """4人分の得点がほぼ同時に揃った際、複数リクエストが並行して確定処理の
    所有権を取ろうとしても、成功するのは1件のみであることを確認する(FEZ-49)
    """
    # Arrange
    hanchan_id = ObjectId()
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=hanchan_id,
    )
    match_repository.create(match)

    concurrency = 5
    results: list = []
    barrier = threading.Barrier(concurrency)

    def claim():
        barrier.wait()
        results.append(match_service.try_clear_active_hanchan(match._id, hanchan_id))

    threads = [threading.Thread(target=claim) for _ in range(concurrency)]

    # Act
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Assert
    assert results.count(True) == 1
    assert results.count(False) == concurrency - 1
    record = match_repository.find({"_id": match._id})[0]
    assert record.active_hanchan_id is None
