import unittest.mock as mock_module
from unittest.mock import MagicMock

from application_service import reply_service, request_info_service
from domain_model.entities.user import User
from domain_model.entities.user_group import UserGroup
from line_models.event import Event
from repositories import user_group_repository, user_repository
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
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"from": "invalid", "to": "invalid"}

    user_repository.create(User(line_user_id=dummy_event.source.user_id, line_user_name="Alice"))
    use_case = ReplyRankingTableUseCase()

    # Act
    use_case.execute()

    # Assert
    texts = [t.text for t in reply_service.texts]
    assert "日付は以下のフォーマットで入力してください。" in texts


def test_execute_targets_group_participants():
    """このグループの対戦参加歴がある全ユーザーを対象にする(メンション不要)。"""
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"from": "invalid", "to": "invalid"}

    # 送信者(友達登録済み) + グループ内の別参加者(未登録=友達ではない)
    user_repository.create(User(line_user_id=dummy_event.source.user_id, line_user_name="Alice"))
    user_group_repository.create(
        UserGroup(
            line_group_id=dummy_event.source.group_id,
            line_user_id=dummy_event.source.user_id,
        ),
    )
    user_group_repository.create(
        UserGroup(
            line_group_id=dummy_event.source.group_id,
            line_user_id="U_NOT_FRIEND_GROUP_MEMBER",
        ),
    )

    use_case = ReplyRankingTableUseCase()

    # Act
    target_user_ids, active_user_line_ids = use_case._resolve_users()

    # Assert: 未登録の参加者は除外され、案内が出る
    assert active_user_line_ids == [dummy_event.source.user_id]
    assert len(target_user_ids) == 1
    texts = [t.text for t in reply_service.texts]
    assert "友達登録されていないユーザは表示されません。" in texts


def test_fetch_profile_images_skips_user_whose_profile_fetch_fails(mocker):
    """1ユーザーのLINEプロフィール取得が失敗しても、グループ全体の応答は継続する。

    グループの過去参加者全員が対象になり得るため、
    ブロック/友達解除済みの1人がget_profile()で例外を出しただけで
    グループ全体がシステムエラーになっていたバグの回帰テスト。
    """
    from use_cases.group_line.reply_ranking_table_use_case import (
        ReplyRankingTableUseCase,
    )

    def fake_get_profile(line_user_id):
        if line_user_id == "U0123456789abcdefghijklmnopqrstu1":
            raise Exception("blocked")
        profile = MagicMock()
        profile.display_name = "Bob"
        profile.picture_url = None
        return profile

    mocker.patch(
        "use_cases.group_line.reply_ranking_table_use_case.line_bot_api.get_profile",
        side_effect=fake_get_profile,
    )

    use_case = ReplyRankingTableUseCase()
    display_name_dict = use_case._fetch_profile_images(
        ["U0123456789abcdefghijklmnopqrstu1", "U0123456789abcdefghijklmnopqrstu2"],
    )

    # 失敗したユーザーもエントリ自体は残る(DBフォールバックの名前、または見つからなければline_id)
    assert display_name_dict["U0123456789abcdefghijklmnopqrstu1"] is not None
    assert display_name_dict["U0123456789abcdefghijklmnopqrstu2"] == "Bob"


def test_success_fail_savefig(mocker):
    """ユーザーが登録済みで日付フィルターなし → 画像生成まで到達するが。

    保存先ディレクトリが存在しない場合は FileNotFoundError が捕捉されて
    システムエラーメッセージが返る。
    PIL・LINE API・urllib3 をモックして外部依存を排除する。
    """
    # Mock PIL Image module
    mock_img = MagicMock()
    mock_img.size = (1024, 768)
    mock_img.save.side_effect = FileNotFoundError("No such file or directory")

    mock_image = MagicMock()
    mock_image.new.return_value = mock_img
    mock_image.open.return_value = mock_img
    mock_image.alpha_composite.return_value = mock_img
    mocker.patch(
        "application_service.ranking_table_image_builder.Image",
        mock_image,
    )

    mock_draw = MagicMock()
    mock_draw.textbbox.return_value = (0, 0, 100, 20)
    mock_image_draw = MagicMock()
    mock_image_draw.Draw.return_value = mock_draw
    mocker.patch(
        "application_service.ranking_table_image_builder.ImageDraw",
        mock_image_draw,
    )
    mocker.patch(
        "application_service.ranking_table_image_builder.ImageFont",
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
