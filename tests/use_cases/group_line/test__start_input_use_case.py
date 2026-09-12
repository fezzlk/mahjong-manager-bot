from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match, MatchStatus
from line_models.event import Event
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
)
from use_cases.group_line.start_input_use_case import StartInputUseCase

dummy_groups = [
    Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    ),
    Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
    ),
]

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="_input",
)


def test_execute_no_group():
    # 目的: test_execute_no_group の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / (
    # reply_service: texts
    # DB操作: group_repository.create(dummy_groups[1])
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    group_repository.create(dummy_groups[1])

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "トークルームが登録されていません。招待し直してください。"
    )


def test_execute_input_mode():
    # 目的: test_execute_input_mode の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "すでに入力モードです。" である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group)
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    dummy_groups1 = [
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.input.value,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
        ),
    ]
    for dummy_group in dummy_groups1:
        group_repository.create(dummy_group)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "すでに入力モードです。"


def test_execute_new_match():
    # 目的: test_execute_new_match の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups の件数が 1 件 / groups[0].current_input_match_id is not None / matches の件数が 1 件 / matches[0].active_hanchan_id is not None / hanchans の件数が 1 件
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); groups = group_repository.find(; matches = match_repository.find(); hanchans = hanchan_repository.find()
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    for dummy_group in dummy_groups:
        group_repository.create(dummy_group)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "第1回戦お疲れ様です。各自点数を入力してください。\n(同点の場合は上家が高くなるように数点追加してください)"
    )
    groups = group_repository.find(
        {"line_group_id": "G0123456789abcdefghijklmnopqrstu1"},
    )
    assert len(groups) == 1
    assert groups[0].current_input_match_id is not None
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is not None
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 1


def test_execute_new_hanchan():
    # 目的: test_execute_new_hanchan の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups の件数が 1 件 / groups[0].current_input_match_id is not None / matches の件数が 1 件 / matches[0].active_hanchan_id is not None / hanchans の件数が 1 件
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); match_repository.create(; groups = group_repository.find(; matches = match_repository.find(); hanchans = hanchan_repository.find()
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    dummy_groups2 = [
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            current_input_match_id=1,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
        ),
    ]
    for dummy_group in dummy_groups2:
        group_repository.create(dummy_group)
    match_repository.create(
        Match(
            _id=1,
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
        ),
    )

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "第1回戦お疲れ様です。各自点数を入力してください。\n(同点の場合は上家が高くなるように数点追加してください)"
    )
    groups = group_repository.find(
        {"line_group_id": "G0123456789abcdefghijklmnopqrstu1"},
    )
    assert len(groups) == 1
    assert groups[0].current_input_match_id is not None
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is not None
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 1


def test_execute_shows_picker_when_multiple_open_matches():
    """openな対戦が2件以上ならピッカーを提示し、どちらにも入力を開始しない
    (FEZ-66 Phase E)。ピッカーには既存対戦に加えて「新しい対戦を始める」
    項目(_new_matchへのpostback)が含まれる。
    """
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    match_repository.create(
        Match(line_group_id=line_group_id, name="対戦A", status=MatchStatus.open.value),
    )
    match_repository.create(
        Match(line_group_id=line_group_id, name="対戦B", status=MatchStatus.open.value),
    )

    StartInputUseCase().execute()

    assert len(reply_service.texts) == 1
    msg = reply_service.texts[0]
    assert msg.quick_reply is not None
    labels = {item.action.label for item in msg.quick_reply.items}
    assert labels == {"対戦A", "対戦B", "新しい対戦を始める"}
    new_match_item = next(
        item for item in msg.quick_reply.items if item.action.label == "新しい対戦を始める"
    )
    assert new_match_item.action.data == "_new_match"
    groups = group_repository.find({"line_group_id": line_group_id})
    assert groups[0].mode == GroupMode.wait.value


def test_select_enters_the_chosen_match():
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    target = match_repository.create(
        Match(line_group_id=line_group_id, name="対戦A", status=MatchStatus.open.value),
    )
    request_info_service.params = {"to": str(target._id)}

    StartInputUseCase().select()

    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "第1回戦お疲れ様です。各自点数を入力してください。\n(同点の場合は上家が高くなるように数点追加してください)"
    )
    groups = group_repository.find({"line_group_id": line_group_id})
    assert groups[0].mode == GroupMode.input.value
    assert groups[0].current_input_match_id == target._id


def test_select_invalid_match_id():
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    request_info_service.params = {"to": "644c838186bbd9e20a91b785"}

    StartInputUseCase().select()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "指定された対戦が見つかりません。"


def test_select_malformed_match_id():
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    request_info_service.params = {"to": "not-a-valid-object-id"}

    StartInputUseCase().select()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "指定された対戦が見つかりません。"


def test_select_blocked_while_already_in_input_mode():
    """ピッカーが古くなり、選択時点で既に別対戦の入力が始まっていた場合は
    ブロックする(stale postback対策)。
    """
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.input.value))
    target = match_repository.create(
        Match(line_group_id=line_group_id, name="対戦A", status=MatchStatus.open.value),
    )
    request_info_service.params = {"to": str(target._id)}

    StartInputUseCase().select()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "すでに入力モードです。"


def test_mode_updated_before_match_creation():
    """Mode が current_input_match_id より先に input に更新されることを確認する。

    レース条件対策として group.mode = input を先に DB へ書き込むため、
    match 作成後も group.mode と current_input_match_id が両方保存されている。
    """
    from unittest.mock import patch

    from domain_service import group_service as gs

    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    for dummy_group in dummy_groups:
        group_repository.create(dummy_group)

    update_calls = []
    original_update = gs.update

    def tracking_update(group):
        update_calls.append(group.mode)
        return original_update(group)

    with patch.object(gs, "update", side_effect=tracking_update):
        use_case.execute()

    # 1回目の update で mode が input に変わっていること
    assert update_calls[0] == GroupMode.input.value
    # 最終的に current_input_match_id も保存されていること
    groups = group_repository.find({"line_group_id": "G0123456789abcdefghijklmnopqrstu1"})
    assert groups[0].mode == GroupMode.input.value
    assert groups[0].current_input_match_id is not None


def test_execute_with_hanchan():
    # 目的: test_execute_with_hanchan の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / ( / groups の件数が 1 件 / groups[0].current_input_match_id is not None / matches の件数が 1 件 / matches[0].active_hanchan_id is not None / hanchans の件数が 1 件
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); match_repository.create(; hanchan_repository.create(; groups = group_repository.find(; matches = match_repository.find(); hanchans = hanchan_repository.find()
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = StartInputUseCase()
    dummy_groups2 = [
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            current_input_match_id=1,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
        ),
    ]
    for dummy_group in dummy_groups2:
        group_repository.create(dummy_group)
    match_repository.create(
        Match(
            _id=1,
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            active_hanchan_id=1,
        ),
    )
    hanchan_repository.create(
        Hanchan(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            match_id=1,
            _id=1,
        ),
    )

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "第1回戦お疲れ様です。各自点数を入力してください。\n(同点の場合は上家が高くなるように数点追加してください)"
    )
    groups = group_repository.find(
        {"line_group_id": "G0123456789abcdefghijklmnopqrstu1"},
    )
    assert len(groups) == 1
    assert groups[0].current_input_match_id is not None
    matches = match_repository.find()
    assert len(matches) == 1
    assert matches[0].active_hanchan_id is not None
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 1
