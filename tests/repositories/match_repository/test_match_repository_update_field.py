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


def test_self_heals_null_parent_field_before_dotted_update():
    """chip_scoresが明示的にnullな既存ドキュメントでも、ドット区切り更新が
    PathNotViableエラーにならず{}へ自己修復した上で更新されることを確認する
    (FEZ-49、Codex review指摘)
    """
    # Arrange
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        chip_scores={"U1": 10},
    )
    match_repository.create(match)
    match_repository.update({"_id": match._id}, {"chip_scores": None})

    # Act
    result = match_repository.update_field(
        {"_id": match._id},
        set_values={"chip_scores.U2": 20},
    )

    # Assert
    assert result.chip_scores == {"U2": 20}


def test_sum_scores_round_trips_through_list_serialization():
    """sum_scoresをupdate_field()経由で更新しても、update()同様list形式で
    永続化され、find()で正しくdictへ復元されることを確認する
    """
    # Arrange
    match = Match(line_group_id="G0123456789abcdefghijklmnopqrstu1")
    match_repository.create(match)

    # Act
    result = match_repository.update_field(
        {"_id": match._id},
        set_values={"sum_scores": {"U1": 50, "U2": -50}},
    )

    # Assert
    assert result.sum_scores == {"U1": 50, "U2": -50}
    record_on_db = match_repository.find({"_id": match._id})[0]
    assert record_on_db.sum_scores == {"U1": 50, "U2": -50}


def test_no_match_returns_none():
    # Act
    result = match_repository.update_field(
        {"_id": ObjectId()},
        set_values={"chip_scores.U1": 10},
    )

    # Assert
    assert result is None


def test_returns_updated_document_when_query_targets_the_changed_field():
    """queryのフィルタ条件自体がこのupdateで変更するフィールドである場合(CAS操作)でも、
    更新後の内容を正しく返すことを確認する(FEZ-49、Codex review指摘)
    """
    # Arrange
    hanchan_id = ObjectId()
    match = Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=hanchan_id,
    )
    match_repository.create(match)

    # Act: active_hanchan_idが現在の値と一致することを条件に、同じフィールドをクリアする
    result = match_repository.update_field(
        {"_id": match._id, "active_hanchan_id": hanchan_id},
        set_values={"active_hanchan_id": None},
    )

    # Assert
    assert result is not None
    assert result.active_hanchan_id is None
    record_on_db = match_repository.find({"_id": match._id})[0]
    assert record_on_db.active_hanchan_id is None


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
