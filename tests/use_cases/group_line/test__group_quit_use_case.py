from application_service import request_info_service
from domain_model.entities.group import Group, GroupMode
from line_models.event import Event
from repositories import group_repository
from use_cases.group_line.group_quit_use_case import GroupQuitUseCase

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    _id=1,
)

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="_exit",
)

def test_fail_no_line_group_id():
    # 目的: test_fail_no_line_group_id の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: groups の件数が 0 件
    # reply_service: なし
    # DB操作: group_repository.create(dummy_group); groups = group_repository.find()
        # Arrange
        use_case = GroupQuitUseCase()
        group_repository.create(dummy_group)
        request_info_service.set_req_info(event=dummy_event)

        # Act
        use_case.execute()

        # Assert
        groups = group_repository.find()
        assert len(groups) == 0
