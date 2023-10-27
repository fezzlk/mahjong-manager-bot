from use_cases.group_line.ReplyHanchansOfActiveMatchUseCase import ReplyHanchansOfActiveMatchUseCase
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Group import Group, GroupMode
from repositories import (
    user_repository,
    hanchan_repository,
    match_repository,
    group_repository,
)
import env_var
from ApplicationService import (
    reply_service,
    request_info_service,
)
import matplotlib.pyplot as plt

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
    active_match_id=1,
    _id=1,
)

dummy_match = Match(
    line_group_id=dummy_group.line_group_id,
    status=2,
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
        status=2,
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
        status=2,
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
        status=2,
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
    status=0,
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
    status=2,
)


def test_success_single_hanchan(mocker):
    # Arrange
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        'subplots',
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        'savefig',
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
    assert reply_service.texts[0].text == '途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。'
    assert reply_service.texts[1].text == "第1回\ntest_user1: +50 (+50)\ntest_user2: +10 (+10)\ntest_user3: -20 (-20)\ntest_user4: -40 (-40)"
    assert len(reply_service.images) == 1
    reply_service.reset()


def test_success_multi_hanchan(mocker):
    # Arrange
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        'subplots',
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        'savefig',
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
    assert reply_service.texts[0].text == '途中経過を表示します。第N回の半荘の削除は「_drop N」と送ってください。'
    assert reply_service.texts[1].text == "第1回\ntest_user1: +50 (+50)\ntest_user2: +10 (+10)\ntest_user3: -20 (-20)\ntest_user4: -40 (-40)\n\n第2回\ntest_user1: +50 (+100)\ntest_user2: +10 (+20)\ntest_user3: -20 (-40)\ntest_user4: -40 (-80)\n\n第3回\ntest_user1: +50 (+150)\ntest_user2: +10 (+30)\ntest_user3: -20 (-60)\ntest_user4: -40 (-120)"
    assert len(reply_service.images) == 1
    reply_service.reset()

def test_success_fail_savefig(mocker):
    # Arrange
    mock = mocker.patch.object(
        reply_service,
        'push_a_message',
    )
    fig, ax = plt.subplots()
    mocker.patch.object(
        plt,
        'subplots',
        return_value=(fig, ax),
    )
    mocker.patch.object(
        fig,
        'savefig',
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
    assert reply_service.texts[0].text == 'システムエラーが発生しました。'
    mock.assert_called_once_with(
        to=env_var.SERVER_ADMIN_LINE_USER_ID,
        message='対戦履歴の画像アップロードに失敗しました\n送信者: test_user1',
    )


def test_success_no_group():
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
    assert reply_service.texts[0].text == 'トークルームが登録されていません。招待し直してください。'


def test_success_no_match():
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
    dummy_match.active_hanchan_id = dummy_active_hanchan._id
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '現在進行中の対戦がありません。'


def test_success_no_hanchans():
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
    assert reply_service.texts[0].text == '現在の対戦で登録済みの半荘がありません。'
