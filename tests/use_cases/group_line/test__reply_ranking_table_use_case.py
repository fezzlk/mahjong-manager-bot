from unittest.mock import MagicMock

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


def test_success_fail_savefig(mocker):
    """
    ユーザーが登録済みで日付フィルターなし → 画像生成まで到達するが、
    保存先ディレクトリが存在しない場合は FileNotFoundError が捕捉されて
    システムエラーメッセージが返る。
    PIL・LINE API・urllib3 をモックして外部依存を排除する。
    """
    # Mock PIL Image module
    mock_img = MagicMock()
    mock_img.size = (1024, 768)
    mock_img.save.side_effect = FileNotFoundError("No such file or directory")

    mock_Image = MagicMock()
    mock_Image.new.return_value = mock_img
    mock_Image.open.return_value = mock_img
    mock_Image.alpha_composite.return_value = mock_img
    mocker.patch(
        "use_cases.group_line.reply_ranking_table_use_case.Image",
        mock_Image,
    )

    mock_draw = MagicMock()
    mock_draw.textbbox.return_value = (0, 0, 100, 20)
    mock_ImageDraw = MagicMock()
    mock_ImageDraw.Draw.return_value = mock_draw
    mocker.patch(
        "use_cases.group_line.reply_ranking_table_use_case.ImageDraw",
        mock_ImageDraw,
    )
    mocker.patch(
        "use_cases.group_line.reply_ranking_table_use_case.ImageFont",
        MagicMock(),
    )

    # Mock LINE API profile fetch
    mock_profile = MagicMock()
    mock_profile.display_name = "Alice"
    mock_profile.picture_url = "http://example.com/img.jpg"
    mocker.patch(
        "use_cases.group_line.reply_ranking_table_use_case.line_bot_api.get_profile",
        return_value=mock_profile,
    )

    # Mock urllib3 profile image download (including file write via mock_open)
    mock_pool = MagicMock()
    mock_pool.request.return_value = MagicMock(data=b"fake_jpeg_data")
    mock_urllib3 = MagicMock()
    mock_urllib3.PoolManager.return_value = mock_pool
    mocker.patch(
        "use_cases.group_line.reply_ranking_table_use_case.urllib3",
        mock_urllib3,
    )

    # Mock built-in open for profile image file write only at the module level
    import unittest.mock as mock_module
    mocker.patch(
        "use_cases.group_line.reply_ranking_table_use_case.open",
        mock_module.mock_open(),
        create=True,
    )

    # Mock push_a_message to prevent real LINE API call
    mocker.patch.object(reply_service, "push_a_message", return_value=None)

    # Arrange: register the requesting user
    user_repository.create(
        User(line_user_id=dummy_event.source.user_id, line_user_name="Alice"),
    )
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {}  # no date filter → parse_date_from_text(None) returns (None, False)
    request_info_service.mention_line_ids = []
    request_info_service.is_mention_all = False

    # Act
    use_case = ReplyRankingTableUseCase()
    use_case.execute()

    # Assert: image save failure triggers system error message
    texts = [t.text for t in reply_service.texts]
    assert "システムエラーが発生しました。" in texts
