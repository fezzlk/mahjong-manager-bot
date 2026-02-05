from domain_model.entities.match import Match
from repositories import match_repository
from use_cases.web.get_match_for_web_use_case import GetMatchForWebUseCase


def test_execute_returns_match_by_id():
    # 目的: test_execute_returns_match_by_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: match is not None / match.line_group_id が "G1" である
    # reply_service: なし
    # DB操作: created = match_repository.create(Match(line_group_id="G1"))
    # Arrange
    created = match_repository.create(Match(line_group_id="G1"))
    use_case = GetMatchForWebUseCase()

    # Act
    match = use_case.execute(created._id)

    # Assert
    assert match is not None
    assert match.line_group_id == "G1"


def test_execute_returns_none_for_missing_id():
    # 目的: test_execute_returns_none_for_missing_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: match is None
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = GetMatchForWebUseCase()

    # Act
    match = use_case.execute("000000000000000000000000")

    # Assert
    assert match is None
