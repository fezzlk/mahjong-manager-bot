from use_cases.common_line.ReplyRankHistoryUseCase import ReplyRankHistoryUseCase
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.UserHanchan import UserHanchan
from DomainModel.entities.Group import Group, GroupMode
from repositories import (
    user_repository,
    user_hanchan_repository,
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
import pytest
from typing import Dict


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
]

dummy_user_hanchans = [
    UserHanchan(
        line_user_id=dummy_users[0].line_user_id,
        hanchan_id=dummy_archived_hanchans[0]._id,
        point=40000,
        rank=1,
    ),
    UserHanchan(
        line_user_id=dummy_users[1].line_user_id,
        hanchan_id=dummy_archived_hanchans[0]._id,
        point=30000,
        rank=2,
    ),
    UserHanchan(
        line_user_id=dummy_users[2].line_user_id,
        hanchan_id=dummy_archived_hanchans[0]._id,
        point=20000,
        rank=3,
    ),
    UserHanchan(
        line_user_id=dummy_users[3].line_user_id,
        hanchan_id=dummy_archived_hanchans[0]._id,
        point=10000,
        rank=4,
    ),
    UserHanchan(
        line_user_id=dummy_users[0].line_user_id,
        hanchan_id=dummy_archived_hanchans[1]._id,
        point=40000,
        rank=1,
    ),
    UserHanchan(
        line_user_id=dummy_users[1].line_user_id,
        hanchan_id=dummy_archived_hanchans[1]._id,
        point=30000,
        rank=2,
    ),
    UserHanchan(
        line_user_id=dummy_users[2].line_user_id,
        hanchan_id=dummy_archived_hanchans[1]._id,
        point=20000,
        rank=3,
    ),
    UserHanchan(
        line_user_id=dummy_users[3].line_user_id,
        hanchan_id=dummy_archived_hanchans[1]._id,
        point=10000,
        rank=4,
    ),
]


@ pytest.fixture(params=[
    {'from': 'x'},
    {'to': 'x'},
    {'from': 'x', 'to': '20220101'},
    {'from': '20220101', 'to': 'x'},
    {'from': 'x', 'to': 'x'},
])
def case1(request) -> Dict[str, str]:
    return request.param

def test_ng_invaild_range_format(case1):
    # Arrange
    use_case = ReplyRankHistoryUseCase()
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.params = case1

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == '日付は以下のフォーマットで入力してください。'
    assert reply_service.texts[1].text == '[日付の入力方法]\n\nYYYY年MM月DD日\n→ YYYYMMDD\n\n20YY年MM月DD日\n→ YYMMDD\n\n今年MM月DD日\n→ MMDD\n\n今月DD日\n→ DD'
     

def test_success(mocker):
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
    use_case = ReplyRankHistoryUseCase()
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_archived_hanchan in dummy_archived_hanchans:
        hanchan_repository.create(dummy_archived_hanchan)
    match_repository.create(dummy_match)
    for dummy_user_hanchan in dummy_user_hanchans:
        user_hanchan_repository.create(dummy_user_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 0
    assert len(reply_service.images) == 2
    reply_service.reset()

@ pytest.fixture(params=[
    ({'from': '20230101'}, '範囲指定: 2023年01月01日から'),
    ({'to': '20241231'}, '範囲指定: 2024年12月31日まで'),
    ({'from': '20230101', 'to': '20241231'}, '範囲指定: 2023年01月01日から2024年12月31日まで'),
])
def case2(request) -> Dict[str, str]:
    return request.param

def test_success_with_range(mocker, case2):
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
    use_case = ReplyRankHistoryUseCase()
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.params = case2[0]
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_archived_hanchan in dummy_archived_hanchans:
        hanchan_repository.create(dummy_archived_hanchan)
    match_repository.create(dummy_match)
    for dummy_user_hanchan in dummy_user_hanchans:
        user_hanchan_repository.create(dummy_user_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == case2[1]
    assert len(reply_service.images) == 2
    reply_service.reset()

def test_success_no_user_hanchan(mocker):
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

    use_case = ReplyRankHistoryUseCase()
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_archived_hanchan in dummy_archived_hanchans:
        hanchan_repository.create(dummy_archived_hanchan)
    match_repository.create(dummy_match)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 0
    assert len(reply_service.images) == 2
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

    use_case = ReplyRankHistoryUseCase()
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)
    for dummy_archived_hanchan in dummy_archived_hanchans:
        hanchan_repository.create(dummy_archived_hanchan)
    match_repository.create(dummy_match)
    for dummy_user_hanchan in dummy_user_hanchans:
        user_hanchan_repository.create(dummy_user_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.images) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == 'システムエラーが発生しました。'
    mock.assert_called_once_with(
        to=env_var.SERVER_ADMIN_LINE_USER_ID,
        message='順位履歴の画像アップロードに失敗しました\n送信者: test_user1',
    )
