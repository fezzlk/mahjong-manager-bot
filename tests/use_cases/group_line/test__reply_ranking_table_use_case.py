from application_service import reply_service, request_info_service
from domain_model.entities.user import User
from line_models.event import Event
from repositories import user_repository
from use_cases.group_line.reply_ranking_table_use_case import ReplyRankingTableUseCase


dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)


def test_execute_with_invalid_date_format():
    # 目的: test_execute_with_invalid_date_format の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: "友達登録されていないユーザは表示されません。" in texts / "日付は以下のフォーマットで入力してください。" in texts
    # reply_service: なし
    # DB操作: user_repository.create(User(line_user_id=dummy_event.source.user_id, line_user_name="Alice"))
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"from": "invalid", "to": "invalid"}
    request_info_service.mention_line_ids = ["U_NOT_FRIEND"]
    request_info_service.is_mention_all = False

    user_repository.create(User(line_user_id=dummy_event.source.user_id, line_user_name="Alice"))
    use_case = ReplyRankingTableUseCase()

    # Act
    use_case.execute()

    # Assert
    texts = [t.text for t in reply_service.texts]
    assert "友達登録されていないユーザは表示されません。" in texts
    assert "日付は以下のフォーマットで入力してください。" in texts


def test_execute_with_mention_all_and_invalid_date():
    # 目的: test_execute_with_mention_all_and_invalid_date の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: "@Allによるメンションでは、このグループでの対戦に参加したことのある全ユーザを対象とします。" in texts / "日付は以下のフォーマットで入力してください。" in texts
    # reply_service: なし
    # DB操作: user_repository.create(User(line_user_id=dummy_event.source.user_id, line_user_name="Alice"))
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"from": "invalid", "to": "invalid"}
    request_info_service.mention_line_ids = []
    request_info_service.is_mention_all = True

    user_repository.create(User(line_user_id=dummy_event.source.user_id, line_user_name="Alice"))
    use_case = ReplyRankingTableUseCase()

    # Act
    use_case.execute()

    # Assert
    texts = [t.text for t in reply_service.texts]
    assert "@Allによるメンションでは、このグループでの対戦に参加したことのある全ユーザを対象とします。" in texts
    assert "日付は以下のフォーマットで入力してください。" in texts
