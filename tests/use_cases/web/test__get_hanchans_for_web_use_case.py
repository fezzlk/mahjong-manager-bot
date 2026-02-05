from domain_model.entities.hanchan import Hanchan
from repositories import hanchan_repository
from use_cases.web.get_hanchans_for_web_use_case import GetHanchansForWebUseCase


def test_execute_returns_hanchans():
    # 目的: test_execute_returns_hanchans の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchans の件数が 2 件
    # reply_service: なし
    # DB操作: hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1)); hanchan_repository.create(Hanchan(line_group_id="G2", match_id=2))
    # Arrange
    hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1))
    hanchan_repository.create(Hanchan(line_group_id="G2", match_id=2))
    use_case = GetHanchansForWebUseCase()

    # Act
    hanchans = use_case.execute()

    # Assert
    assert len(hanchans) == 2


def test_execute_returns_empty_list():
    # 目的: test_execute_returns_empty_list の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchans が [] である
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = GetHanchansForWebUseCase()

    # Act
    hanchans = use_case.execute()

    # Assert
    assert hanchans == []
