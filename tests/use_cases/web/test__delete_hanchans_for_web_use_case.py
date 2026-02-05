from domain_model.entities.hanchan import Hanchan
from repositories import hanchan_repository
from use_cases.web.delete_hanchans_for_web_use_case import DeleteHanchansForWebUseCase


def test_execute_deletes_hanchans_by_ids():
    # 目的: test_execute_deletes_hanchans_by_ids の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: remaining の件数が 1 件 / remaining[0].line_group_id が "G2" である
    # reply_service: なし
    # DB操作: h1 = hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1)); h2 = hanchan_repository.create(Hanchan(line_group_id="G2", match_id=2)); remaining = hanchan_repository.find()
    # Arrange
    h1 = hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1))
    h2 = hanchan_repository.create(Hanchan(line_group_id="G2", match_id=2))
    use_case = DeleteHanchansForWebUseCase()

    # Act
    use_case.execute([h1._id])

    # Assert
    remaining = hanchan_repository.find()
    assert len(remaining) == 1
    assert remaining[0].line_group_id == "G2"


def test_execute_with_empty_ids_does_nothing():
    # 目的: test_execute_with_empty_ids_does_nothing の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: remaining の件数が 1 件
    # reply_service: なし
    # DB操作: hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1)); remaining = hanchan_repository.find()
    # Arrange
    hanchan_repository.create(Hanchan(line_group_id="G1", match_id=1))
    use_case = DeleteHanchansForWebUseCase()

    # Act
    use_case.execute([])

    # Assert
    remaining = hanchan_repository.find()
    assert len(remaining) == 1
