import threading

from bson.objectid import ObjectId

from domain_model.entities.match import Match
from repositories import match_repository


def test_set_new_field_path():
    # Arrange
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        chip_scores={"U1": 10},
    )
    match_repository.create(match)

    # Act
    result = match_repository.update_field(
        {"_id": match._id},
        set_values={"chip_scores.U2": 20},
    )

    # Assert
    assert result.chip_scores == {"U1": 10, "U2": 20}
    record_on_db = match_repository.find({"_id": match._id})[0]
    assert record_on_db.chip_scores == {"U1": 10, "U2": 20}


def test_unset_field_path():
    # Arrange
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        chip_scores={"U1": 10, "U2": 20},
    )
    match_repository.create(match)

    # Act
    result = match_repository.update_field(
        {"_id": match._id},
        unset_fields=["chip_scores.U1"],
    )

    # Assert
    assert result.chip_scores == {"U2": 20}


def test_no_match_returns_none():
    # Act
    result = match_repository.update_field(
        {"_id": ObjectId()},
        set_values={"chip_scores.U1": 10},
    )

    # Assert
    assert result is None


def test_concurrent_writes_do_not_overwrite_each_other():
    """4人がほぼ同時にチップを入力しても全員分のデータが欠落なく保存されることを確認する(FEZ-49)"""
    # Arrange
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        chip_scores={},
    )
    match_repository.create(match)

    line_user_ids = ["U1", "U2", "U3", "U4"]
    barrier = threading.Barrier(len(line_user_ids))

    def submit(line_user_id: str, score: int):
        barrier.wait()
        match_repository.update_field(
            {"_id": match._id},
            set_values={f"chip_scores.{line_user_id}": score},
        )

    threads = [
        threading.Thread(target=submit, args=(uid, i + 1))
        for i, uid in enumerate(line_user_ids)
    ]

    # Act
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Assert
    record_on_db = match_repository.find({"_id": match._id})[0]
    assert len(record_on_db.chip_scores) == 4
    for i, uid in enumerate(line_user_ids):
        assert record_on_db.chip_scores[uid] == i + 1
