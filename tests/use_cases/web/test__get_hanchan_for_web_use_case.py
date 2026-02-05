from domain_model.entities.hanchan import Hanchan
from repositories import hanchan_repository
from use_cases.web.get_hanchan_for_web_use_case import GetHanchanForWebUseCase


def test_execute_returns_hanchan_by_id():
    # 目的: test_execute_returns_hanchan_by_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchan is not None / hanchan.line_group_id が "G1" である
    # reply_service: なし
    # DB操作: created = hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1))
    # Arrange
    created = hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1))
    use_case = GetHanchanForWebUseCase()

    # Act
    hanchan = use_case.execute(created._id)

    # Assert
    assert hanchan is not None
    assert hanchan.line_group_id == "G1"


def test_execute_returns_none_for_missing_id():
    # 目的: test_execute_returns_none_for_missing_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchan is None
    # reply_service: なし
    # DB操作: なし
    # Arrange
    use_case = GetHanchanForWebUseCase()

    # Act
    hanchan = use_case.execute("000000000000000000000000")

    # Assert
    assert hanchan is None
