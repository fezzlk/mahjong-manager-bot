from domain_model.entities.match import Match
from repositories import match_repository
from use_cases.web.delete_matches_for_web_use_case import DeleteMatchesForWebUseCase


def test_execute_deletes_matches_by_ids():
    # 目的: test_execute_deletes_matches_by_ids の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: remaining の件数が 1 件 / remaining[0].line_group_id が "G2" である
    # reply_service: なし
    # DB操作: m1 = match_repository.create(Match(line_group_id="G1")); m2 = match_repository.create(Match(line_group_id="G2")); remaining = match_repository.find()
    # Arrange
    m1 = match_repository.create(Match(line_group_id="G1"))
    match_repository.create(Match(line_group_id="G2"))
    use_case = DeleteMatchesForWebUseCase()

    # Act
    use_case.execute([m1._id])

    # Assert
    remaining = match_repository.find()
    assert len(remaining) == 1
    assert remaining[0].line_group_id == "G2"


def test_execute_with_empty_ids_does_nothing():
    # 目的: test_execute_with_empty_ids_does_nothing の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: remaining の件数が 1 件
    # reply_service: なし
    # DB操作: match_repository.create(Match(line_group_id="G1")); remaining = match_repository.find()
    # Arrange
    match_repository.create(Match(line_group_id="G1"))
    use_case = DeleteMatchesForWebUseCase()

    # Act
    use_case.execute([])

    # Assert
    remaining = match_repository.find()
    assert len(remaining) == 1
