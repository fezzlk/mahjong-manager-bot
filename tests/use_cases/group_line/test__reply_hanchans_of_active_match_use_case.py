import matplotlib.pyplot as plt

import env_var
from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match, MatchStatus
from domain_model.entities.user import User, UserMode
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
    user_repository,
)
from use_cases.group_line.reply_hanchans_of_active_match_use_case import (
    ReplyHanchansOfActiveMatchUseCase,
)

dummy_users = [
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        mode=UserMode.wait.value,
        jantama_name="jantama_user1",
        _id=1,
    ),
    User(
        line_user_name="test_user2",
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        mode=UserMode.wait.value,
        jantama_name="jantama_user2",
        _id=2,
    ),
    User(
        line_user_name="test_user3",
        line_user_id="U0123456789abcdefghijklmnopqrstu3",
        mode=UserMode.wait.value,
        jantama_name="jantama_user3",
        _id=3,
    ),
    User(
        line_user_name="test_user4",
        line_user_id="U0123456789abcdefghijklmnopqrstu4",
        mode=UserMode.wait.value,
        jantama_name="jantama_user4",
        _id=4,
    ),
    User(
        line_user_name="test_user5",
        line_user_id="U0123456789abcdefghijklmnopqrstu5",
        mode=UserMode.wait.value,
        jantama_name="jantama_user5",
        _id=5,
    ),
]

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    current_input_match_id=1,
    _id=1,
)

dummy_match = Match(
    line_group_id=dummy_group.line_group_id,
    _id=1,
)

dummy_archived_hanchans = [
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[0].line_user_id: 40000,
            dummy_users[1].line_user_id: 30000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 10000,
        },
        converted_scores={
            dummy_users[0].line_user_id: 50,
            dummy_users[1].line_user_id: 10,
            dummy_users[2].line_user_id: -20,
            dummy_users[3].line_user_id: -40,
        },
        match_id=1,
        _id=1,
    ),
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[0].line_user_id: 40000,
            dummy_users[1].line_user_id: 30000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 10000,
        },
        converted_scores={
            dummy_users[0].line_user_id: 50,
            dummy_users[1].line_user_id: 10,
            dummy_users[2].line_user_id: -20,
            dummy_users[3].line_user_id: -40,
        },
        match_id=1,
        _id=2,
    ),
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[0].line_user_id: 40000,
            dummy_users[1].line_user_id: 30000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 10000,
        },
        converted_scores={
            dummy_users[0].line_user_id: 50,
            dummy_users[1].line_user_id: 10,
            dummy_users[2].line_user_id: -20,
            dummy_users[3].line_user_id: -40,
        },
        match_id=1,
        _id=3,
    ),
]

dummy_disabled_hanchan = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 40000,
        dummy_users[1].line_user_id: 30000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[3].line_user_id: 10000,
    },
    converted_scores={
        dummy_users[0].line_user_id: 50,
        dummy_users[1].line_user_id: 10,
        dummy_users[2].line_user_id: -20,
        dummy_users[3].line_user_id: -40,
    },
    match_id=1,
    is_deleted=True,
)

dummy_active_hanchan = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={
        dummy_users[0].line_user_id: 40010,
        dummy_users[1].line_user_id: 30000,
        dummy_users[2].line_user_id: 20000,
        dummy_users[3].line_user_id: 10000,
    },
    converted_scores={},
    match_id=1,
)


def test_success_single_hanchan(mocker):
    # 目的: test_success_single_hanchan の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / reply_service.texts[0].text が "途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。" である / reply_service.texts[1].text が "第1回\ntest_user1: +50 (+50)\ntest_user2: +10 (+10)\ntest_user3: -20 (-20)\ntest_user4: -40 (-40)" である / reply_service.images の件数が 1 件
    # reply_service: images, texts
    # DB操作: group_repository.create(dummy_group); user_repository.create(dummy_user); hanchan_repository.create(dummy_archived_hanchans[0]); hanchan_repository.create(dummy_disabled_hanchan); hanchan_repository.create(dummy_active_hanchan); match_repository.create(dummy_match)
    # Arrange
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        "subplots",
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        "savefig",
    )
    use_case = ReplyHanchansOfActiveMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_archived_hanchans[0])
    hanchan_repository.create(dummy_disabled_hanchan)
    hanchan_repository.create(dummy_active_hanchan)
    dummy_match.active_hanchan_id = dummy_active_hanchan._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == "途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。"
    assert reply_service.texts[1].text == "第1回\ntest_user1: +50 (+50)\ntest_user2: +10 (+10)\ntest_user3: -20 (-20)\ntest_user4: -40 (-40)"
    assert len(reply_service.images) == 1
    reply_service.reset()

def test_success_contain_unknown_user(mocker):
    # 目的: test_success_contain_unknown_user の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / reply_service.texts[0].text が "途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。" である / reply_service.texts[1].text が "第1回\n友達未登録: +50 (+50)\n友達未登録: +10 (+10)\n友達未登録: -20 (-20)\n友達未登録: -40 (-40)" である / reply_service.images の件数が 1 件
    # reply_service: images, texts
    # DB操作: group_repository.create(dummy_group); # user_repository.create(dummy_user); hanchan_repository.create(dummy_archived_hanchans[0]); hanchan_repository.create(dummy_disabled_hanchan); hanchan_repository.create(dummy_active_hanchan); match_repository.create(dummy_match)
    # Arrange
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        "subplots",
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        "savefig",
    )
    use_case = ReplyHanchansOfActiveMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    # for dummy_user in dummy_users:
    #     user_repository.create(dummy_user)
    hanchan_repository.create(dummy_archived_hanchans[0])
    hanchan_repository.create(dummy_disabled_hanchan)
    hanchan_repository.create(dummy_active_hanchan)
    dummy_match.active_hanchan_id = dummy_active_hanchan._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == "途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。"
    assert reply_service.texts[1].text == "第1回\n友達未登録: +50 (+50)\n友達未登録: +10 (+10)\n友達未登録: -20 (-20)\n友達未登録: -40 (-40)"
    assert len(reply_service.images) == 1
    reply_service.reset()


def test_success_multi_hanchan(mocker):
    # 目的: test_success_multi_hanchan の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 2 件 / reply_service.texts[0].text が "途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。" である / reply_service.texts[1].text が "第1回\ntest_user1: +50 (+50)\ntest_user2: +10 (+10)\ntest_user3: -20 (-20)\ntest_user4: -40 (-40)\n\n第2回\ntest_user1: +50 (+100)\ntest_user2: +10 (+20)\ntest_user3: -20 (-40)\ntest_user4: -40 (-80)\n\n第3回\ntest_user1: +50 (+150)\ntest_user2: +10 (+30)\ntest_user3: -20 (-60)\ntest_user4: -40 (-120)" である / reply_service.images の件数が 1 件
    # reply_service: images, texts
    # DB操作: group_repository.create(dummy_group); user_repository.create(dummy_user); hanchan_repository.create(dummy_archived_hanchan); hanchan_repository.create(dummy_disabled_hanchan); hanchan_repository.create(dummy_active_hanchan); match_repository.create(dummy_match)
    # Arrange
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        "subplots",
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        "savefig",
    )

    use_case = ReplyHanchansOfActiveMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_archived_hanchan in dummy_archived_hanchans:
        hanchan_repository.create(dummy_archived_hanchan)
    hanchan_repository.create(dummy_disabled_hanchan)
    hanchan_repository.create(dummy_active_hanchan)
    dummy_match.active_hanchan_id = dummy_active_hanchan._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == "途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。"
    assert reply_service.texts[1].text == "第1回\ntest_user1: +50 (+50)\ntest_user2: +10 (+10)\ntest_user3: -20 (-20)\ntest_user4: -40 (-40)\n\n第2回\ntest_user1: +50 (+100)\ntest_user2: +10 (+20)\ntest_user3: -20 (-40)\ntest_user4: -40 (-80)\n\n第3回\ntest_user1: +50 (+150)\ntest_user2: +10 (+30)\ntest_user3: -20 (-60)\ntest_user4: -40 (-120)"
    assert len(reply_service.images) == 1
    reply_service.reset()

def test_success_fail_savefig(mocker):
    # 目的: test_success_fail_savefig の挙動を検証する。
    # 入力: mocker
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.images の件数が 0 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "システムエラーが発生しました。" である
    # reply_service: images, texts
    # DB操作: group_repository.create(dummy_group); user_repository.create(dummy_user); hanchan_repository.create(dummy_archived_hanchan); hanchan_repository.create(dummy_disabled_hanchan); hanchan_repository.create(dummy_active_hanchan); match_repository.create(dummy_match)
    # Arrange
    mock = mocker.patch.object(
        reply_service,
        "push_a_message",
    )
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        "subplots",
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        "savefig",
        side_effect=FileNotFoundError(),
    )

    use_case = ReplyHanchansOfActiveMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_archived_hanchan in dummy_archived_hanchans:
        hanchan_repository.create(dummy_archived_hanchan)
    hanchan_repository.create(dummy_disabled_hanchan)
    hanchan_repository.create(dummy_active_hanchan)
    dummy_match.active_hanchan_id = dummy_active_hanchan._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.images) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "システムエラーが発生しました。"
    call_kwargs = mock.call_args.kwargs
    assert call_kwargs["to"] == env_var.SERVER_ADMIN_LINE_USER_ID
    assert "送信者: test_user1" in call_kwargs["message"]


def test_success_no_group():
    # 目的: test_success_no_group の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "トークルームが登録されていません。招待し直してください。" である
    # reply_service: texts
    # DB操作: user_repository.create(dummy_user); hanchan_repository.create(dummy_archived_hanchans[0]); hanchan_repository.create(dummy_disabled_hanchan); hanchan_repository.create(dummy_active_hanchan); match_repository.create(dummy_match)
    # Arrange
    use_case = ReplyHanchansOfActiveMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_archived_hanchans[0])
    hanchan_repository.create(dummy_disabled_hanchan)
    hanchan_repository.create(dummy_active_hanchan)
    dummy_match.active_hanchan_id = dummy_active_hanchan._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "トークルームが登録されていません。招待し直してください。"


def test_success_no_match():
    """openな対戦が1件もなければ「進行中の対戦がありません」を返す。

    「どの対戦が進行中か」の正本はMatch.statusであり(FEZ-66 Phase D/E)、
    group.current_input_match_idが未設定かどうかとは無関係。
    """
    # Arrange
    use_case = ReplyHanchansOfActiveMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    no_match_group = Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        mode=GroupMode.input.value,
        _id=1,
    )
    group_repository.create(no_match_group)
    hanchan_repository.create(dummy_archived_hanchans[0])
    hanchan_repository.create(dummy_disabled_hanchan)
    hanchan_repository.create(dummy_active_hanchan)
    # openな対戦を作らず、Matchを一切作成しない。

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "現在進行中の対戦がありません。"


def test_execute_shows_picker_when_multiple_open_matches():
    """openな対戦が2件以上ならピッカーを表示する(FEZ-66 Phase E)。"""
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    match_repository.create(
        Match(line_group_id=line_group_id, name="対戦A", status=MatchStatus.open.value),
    )
    match_repository.create(
        Match(line_group_id=line_group_id, name="対戦B", status=MatchStatus.open.value),
    )
    request_info_service.req_line_group_id = line_group_id

    ReplyHanchansOfActiveMatchUseCase().execute()

    assert len(reply_service.texts) == 1
    msg = reply_service.texts[0]
    assert msg.quick_reply is not None
    labels = {item.action.label for item in msg.quick_reply.items}
    assert labels == {"対戦A", "対戦B"}


def test_select_shows_the_chosen_match(mocker):
    fig, ax = plt.subplots()
    mocker.patch.object(plt, "subplots", return_value=(fig, ax))
    mocker.patch.object(fig, "savefig")

    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    target = match_repository.create(
        Match(line_group_id=line_group_id, name="対戦A", status=MatchStatus.open.value),
    )
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(
        Hanchan(
            line_group_id=line_group_id,
            raw_scores={},
            converted_scores={dummy_users[0].line_user_id: 50},
            match_id=target._id,
        ),
    )
    request_info_service.req_line_group_id = line_group_id
    request_info_service.params = {"to": str(target._id)}

    ReplyHanchansOfActiveMatchUseCase().select()

    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == "途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。"
    reply_service.reset()


def test_select_invalid_match_id():
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    request_info_service.req_line_group_id = line_group_id
    request_info_service.params = {"to": "644c838186bbd9e20a91b785"}

    ReplyHanchansOfActiveMatchUseCase().select()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "指定された対戦が見つかりません。"


def test_select_malformed_match_id():
    line_group_id = "G0123456789abcdefghijklmnopqrstu1"
    group_repository.create(Group(line_group_id=line_group_id, mode=GroupMode.wait.value))
    request_info_service.req_line_group_id = line_group_id
    request_info_service.params = {"to": "not-a-valid-object-id"}

    ReplyHanchansOfActiveMatchUseCase().select()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "指定された対戦が見つかりません。"


def test_success_no_hanchans():
    # 目的: test_success_no_hanchans の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "現在の対戦で登録済みの半荘がありません。" である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); user_repository.create(dummy_user); hanchan_repository.create(dummy_disabled_hanchan); hanchan_repository.create(dummy_active_hanchan); match_repository.create(dummy_match)
    # Arrange
    use_case = ReplyHanchansOfActiveMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    hanchan_repository.create(dummy_disabled_hanchan)
    hanchan_repository.create(dummy_active_hanchan)
    dummy_match.active_hanchan_id = dummy_active_hanchan._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "現在の対戦で登録済みの半荘がありません。"
