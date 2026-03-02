
from application_service import reply_service, request_info_service
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from line_models.event import Event
from mongo_client import hanchans_collection, matches_collection
from repositories import hanchan_repository, match_repository
from use_cases.group_line.drop_match_by_index_use_case import DropMatchByIndexUseCase

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)


def test_execute_with_non_digit_index():
    # 目的: test_execute_with_non_digit_index の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "引数は整数で指定してください。" である
    # reply_service: texts
    # DB操作: なし
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = DropMatchByIndexUseCase()

    # Act
    use_case.execute("abc")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "引数は整数で指定してください。"


def test_execute_drop_archived_match_by_index():
    # 目的: test_execute_drop_archived_match_by_index の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "第1回の対戦結果を削除しました。" である / updated_match.status が 0 である / all(h.status が 0 for h in updated_hanchans) である
    # reply_service: texts
    # DB操作: match_repository.create(match); hanchan_repository.create(hanchan); updated_match = match_repository.find({"_id": match._id})[0]; updated_hanchans = hanchan_repository.find({"match_id": match._id})
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = DropMatchByIndexUseCase()

    match = Match(
        line_group_id=dummy_event.source.group_id,
        sum_prices_with_chip={"U1": 10},
    )
    match_repository.create(match)

    hanchan = Hanchan(
        line_group_id=dummy_event.source.group_id,
        match_id=match._id,
        converted_scores={"U1": 10},
    )
    hanchan_repository.create(hanchan)

    # Act
    use_case.execute("1")

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "第1回の対戦結果を削除しました。"

    updated_match_doc = matches_collection.find_one({"_id": match._id})
    assert updated_match_doc["is_deleted"]

    updated_hanchan_docs = list(hanchans_collection.find({"match_id": match._id}))
    assert all(h["is_deleted"] for h in updated_hanchan_docs)
