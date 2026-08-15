import threading

from bson.objectid import ObjectId

from domain_model.entities.hanchan import Hanchan
from repositories import hanchan_repository


def test_set_new_field_path():
    # Arrange
    hanchan = Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=ObjectId(),
        raw_scores={"U1": 10000},
    )
    hanchan_repository.create(hanchan)

    # Act
    result = hanchan_repository.update_field(
        {"_id": hanchan._id},
        set_values={"raw_scores.U2": 20000},
    )

    # Assert
    assert result.raw_scores == {"U1": 10000, "U2": 20000}
    record_on_db = hanchan_repository.find({"_id": hanchan._id})[0]
    assert record_on_db.raw_scores == {"U1": 10000, "U2": 20000}


def test_unset_field_path():
    # Arrange
    hanchan = Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=ObjectId(),
        raw_scores={"U1": 10000, "U2": 20000},
    )
    hanchan_repository.create(hanchan)

    # Act
    result = hanchan_repository.update_field(
        {"_id": hanchan._id},
        unset_fields=["raw_scores.U1"],
    )

    # Assert
    assert result.raw_scores == {"U2": 20000}


def test_no_match_returns_none():
    # Act
    result = hanchan_repository.update_field(
        {"_id": ObjectId()},
        set_values={"raw_scores.U1": 10000},
    )

    # Assert
    assert result is None


def test_concurrent_writes_do_not_overwrite_each_other():
    """4人がほぼ同時に点数を入力しても全員分のデータが欠落なく保存されることを確認する(FEZ-49)"""
    # Arrange
    hanchan = Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=ObjectId(),
        raw_scores={},
    )
    hanchan_repository.create(hanchan)

    line_user_ids = ["U1", "U2", "U3", "U4"]
    barrier = threading.Barrier(len(line_user_ids))

    def submit(line_user_id: str, score: int):
        barrier.wait()
        hanchan_repository.update_field(
            {"_id": hanchan._id},
            set_values={f"raw_scores.{line_user_id}": score},
        )

    threads = [
        threading.Thread(target=submit, args=(uid, (i + 1) * 1000))
        for i, uid in enumerate(line_user_ids)
    ]

    # Act
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Assert
    record_on_db = hanchan_repository.find({"_id": hanchan._id})[0]
    assert len(record_on_db.raw_scores) == 4
    for i, uid in enumerate(line_user_ids):
        assert record_on_db.raw_scores[uid] == (i + 1) * 1000
