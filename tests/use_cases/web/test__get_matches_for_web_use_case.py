from domain_model.entities.match import Match
from repositories import match_repository
from use_cases.web.get_matches_for_web_use_case import GetMatchesForWebUseCase


def test_execute_returns_matches():
    # 目的: test_execute_returns_matches の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: matches の件数が 2 件
    # reply_service: なし
    # DB操作: match_repository.create(Match(line_group_id="G1")); match_repository.create(Match(line_group_id="G2"))
    # Arrange
    match_repository.create(Match(line_group_id="G1"))
    match_repository.create(Match(line_group_id="G2"))
    use_case = GetMatchesForWebUseCase()

    # Act
    matches = use_case.execute()

    # Assert
    assert len(matches) == 2


def test_execute_returns_empty_list():
    # 目的: test_execute_returns_empty_list の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: matches が [] である
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = GetMatchesForWebUseCase()

    # Act
    matches = use_case.execute()

    # Assert
    assert matches == []
