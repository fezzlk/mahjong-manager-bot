from pathlib import Path

from application_service import reply_service, request_info_service
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match
from domain_model.entities.user import User
from line_models.event import Event
from repositories import hanchan_repository, match_repository, user_repository
from use_cases.group_line.create_match_detail_graph_use_case import (
    CreateMatchDetailGraphUseCase,
)


dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)


def test_execute_returns_image_url():
    # 目的: test_execute_returns_image_url の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: image_url is not None / f"/match_detail/{match._id!s}.png" in image_url
    # reply_service: なし
    # DB操作: user_repository.create(user); match_repository.create(match); hanchan_repository.create(hanchan)
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = CreateMatchDetailGraphUseCase()

    user = User(line_user_id="U1", line_user_name="Alice")
    user_repository.create(user)

    match = Match(line_group_id=dummy_event.source.group_id)
    match_repository.create(match)

    hanchan = Hanchan(
        line_group_id=dummy_event.source.group_id,
        match_id=match._id,
        converted_scores={"U1": 10},
    )
    hanchan_repository.create(hanchan)

    # Act
    image_url = use_case.execute(match._id)

    # Assert
    assert image_url is not None
    assert f"/match_detail/{match._id!s}.png" in image_url


def test_execute_handles_file_write_error():
    # 目的: test_execute_handles_file_write_error の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: image_url is None / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "システムエラーが発生しました。" である
    # reply_service: texts
    # DB操作: user_repository.create(user); match_repository.create(match); hanchan_repository.create(hanchan)
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = CreateMatchDetailGraphUseCase()

    user = User(line_user_id="U1", line_user_name="Alice")
    user_repository.create(user)

    match = Match(line_group_id=dummy_event.source.group_id)
    match_repository.create(match)

    hanchan = Hanchan(
        line_group_id=dummy_event.source.group_id,
        match_id=match._id,
        converted_scores={"U1": 10},
    )
    hanchan_repository.create(hanchan)

    uploads_dir = Path("src/uploads/match_detail")
    backup_dir = Path("src/uploads/_match_detail_backup")
    if uploads_dir.exists():
        uploads_dir.rename(backup_dir)

    try:
        # Act
        image_url = use_case.execute(match._id)
    finally:
        if backup_dir.exists():
            backup_dir.rename(uploads_dir)

    # Assert
    assert image_url is None
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "システムエラーが発生しました。"
