from typing import Dict, Tuple
import pytest
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Group import Group, GroupMode
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from use_cases.group_line.AddPointByTextUseCase import AddPointByTextUseCase
from ApplicationService import (
    reply_service,
    request_info_service,
)
from repositories import (
    hanchan_repository,
    match_repository,
    user_repository,
    group_repository,
)

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    active_match_id=1,
    _id=1,
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

dummy_hanchans = [
    Hanchan(  # 新規追加
        line_group_id=dummy_group.line_group_id,
        raw_scores={},
        converted_scores={},
        match_id=1,
        status=2,
        _id=1,
    ),
    Hanchan(  # 更新
        line_group_id=dummy_group.line_group_id,
        raw_scores={dummy_users[0].line_user_id: 2000},
        converted_scores={},
        match_id=1,
        status=2,
        _id=2,
    ),
    Hanchan(  # 別ユーザー新規追加
        line_group_id=dummy_group.line_group_id,
        raw_scores={dummy_users[1].line_user_id: 2000},
        converted_scores={},
        match_id=1,
        status=2,
        _id=2,
    ),
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[1].line_user_id: 10000,
            dummy_users[2].line_user_id: 10000,
            dummy_users[3].line_user_id: 10000,
        },
        converted_scores={},
        match_id=1,
        status=2,
        _id=1,
    ),
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[1].line_user_id: 10000,
            dummy_users[2].line_user_id: 10000,
            dummy_users[3].line_user_id: 10000,
            dummy_users[4].line_user_id: 10000,
        },
        converted_scores={},
        match_id=1,
        status=2,
        _id=1,
    ),
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[1].line_user_id: 10000,
            dummy_users[2].line_user_id: 10000,
            dummy_users[3].line_user_id: 10000,
            dummy_users[4].line_user_id: 10000,
        },
        converted_scores={},
        match_id=1,
        status=2,
        _id=0,
    ),
]


dummy_match = Match(
    line_group_id=dummy_group.line_group_id,
    status=2,
    _id=1,
)


@ pytest.fixture(params=[
    # (
    #   index of dummy_hanchan,
    #   sent_text,
    #   expected_reply,
    # )
    (0, '1000', 'test_user1: 1000', {dummy_users[0].line_user_id: 1000}),
    (1, '2000', 'test_user1: 2000', {dummy_users[0].line_user_id: 2000}),
    (2, '1000', 'test_user2: 2000\ntest_user1: 1000', {
     dummy_users[0].line_user_id: 1000, dummy_users[1].line_user_id: 2000}),
    (0, '-1000', 'test_user1: -1000', {dummy_users[0].line_user_id: -1000}),
])
def case1(request) -> Tuple[int, str, str, Dict[str, str]]:
    return request.param


def test_execute(case1):
    # Arrange
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    hanchan_repository.create(dummy_hanchans[case1[0]])
    hanchan_repository.create(dummy_hanchans[5])
    dummy_match.active_hanchan_id = dummy_hanchans[case1[0]]._id
    match_repository.create(dummy_match)
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text=case1[1])

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == case1[2]
    hanchans = hanchan_repository.find({'_id': dummy_hanchans[case1[0]]._id})
    expected_raw_scores = case1[3]
    assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
    for k in expected_raw_scores:
        assert hanchans[0].raw_scores[k] == expected_raw_scores[k]


@ pytest.fixture(params=[
    # sent_text,
    'hoge',
])
def case2(request) -> str:
    return request.param


def test_execute_not_int_point(case2):
    # Arrange
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    hanchan_repository.create(dummy_hanchans[1])
    dummy_match.active_hanchan_id = dummy_hanchans[1]._id
    match_repository.create(dummy_match)
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text=case2)

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == '整数で入力してください。'
    hanchans = hanchan_repository.find()
    expected_raw_scores = dummy_hanchans[1].raw_scores
    assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
    for k in expected_raw_scores:
        assert hanchans[0].raw_scores[k] == expected_raw_scores[k]


def test_execute_with_mention():
    # Arrange
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.mention_line_ids = [
        'U0123456789abcdefghijklmnopqrstu1']
    hanchan_repository.create(dummy_hanchans[0])
    dummy_match.active_hanchan_id = dummy_hanchans[0]._id
    match_repository.create(dummy_match)
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text='@test_user1 1000')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == 'test_user1: 1000'
    hanchans = hanchan_repository.find()
    expected_raw_scores = {'U0123456789abcdefghijklmnopqrstu1': 1000}
    assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
    for k in expected_raw_scores:
        assert hanchans[0].raw_scores[k] == expected_raw_scores[k]


def test_execute_multi_mentions():
    # Arrange
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.mention_line_ids = [
        'U0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu2',
    ]
    hanchan_repository.create(dummy_hanchans[0])
    dummy_match.active_hanchan_id = dummy_hanchans[0]._id
    match_repository.create(dummy_match)
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text='@dummy1 @dummy2 1000')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == 'メンションは1回につき1人を指定するようにしてください。'
    hanchans = hanchan_repository.find()
    assert len(hanchans[0].raw_scores) == 0


def test_execute_not_registered_user():
    # Arrange
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.mention_line_ids = ['dummy_line_id']
    hanchan_repository.create(dummy_hanchans[0])
    dummy_match.active_hanchan_id = dummy_hanchans[0]._id
    match_repository.create(dummy_match)
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text='@dummy 1000')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == '友達未登録: 1000'
    hanchans = hanchan_repository.find()
    expected_raw_scores = {'dummy_line_id': 1000}
    assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
    for k in expected_raw_scores:
        assert hanchans[0].raw_scores[k] == expected_raw_scores[k]


def test_execute_fourth_input():
    # Arrange
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    hanchan_repository.create(dummy_hanchans[3])
    dummy_match.active_hanchan_id = dummy_hanchans[3]._id
    match_repository.create(dummy_match)
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text='10000')

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == 'test_user2: 10000\ntest_user3: 10000\ntest_user4: 10000\ntest_user1: 10000'
    assert reply_service.texts[1].type == 'text'
    assert reply_service.texts[1].text == '点数の合計が40000点です。合計100000点+αになるように修正してください。'
    hanchans = hanchan_repository.find()
    expected_raw_scores = {
        dummy_users[0].line_user_id: 10000,
        dummy_users[1].line_user_id: 10000,
        dummy_users[2].line_user_id: 10000,
        dummy_users[3].line_user_id: 10000,
    }
    assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
    for k in expected_raw_scores:
        assert hanchans[0].raw_scores[k] == expected_raw_scores[k]


def test_execute_fifth_input():
    # Arrange
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    hanchan_repository.create(dummy_hanchans[4])
    dummy_match.active_hanchan_id = dummy_hanchans[4]._id
    match_repository.create(dummy_match)
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text='10000')

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == 'test_user2: 10000\ntest_user3: 10000\ntest_user4: 10000\ntest_user5: 10000\ntest_user1: 10000'
    assert reply_service.texts[1].type == 'text'
    assert reply_service.texts[1].text == '5人以上入力されています。@[ユーザー名] で不要な入力を消してください。'
    hanchans = hanchan_repository.find()
    expected_raw_scores = {
        dummy_users[0].line_user_id: 10000,
        dummy_users[1].line_user_id: 10000,
        dummy_users[2].line_user_id: 10000,
        dummy_users[3].line_user_id: 10000,
        dummy_users[4].line_user_id: 10000,
    }
    assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
    for k in expected_raw_scores:
        assert hanchans[0].raw_scores[k] == expected_raw_scores[k]


def test_execute_delete():
    # Arrange
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[1].line_user_id
    hanchan_repository.create(dummy_hanchans[3])
    dummy_match.active_hanchan_id = dummy_hanchans[3]._id
    match_repository.create(dummy_match)
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text='-')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == 'test_user3: 10000\ntest_user4: 10000'
    hanchans = hanchan_repository.find()
    expected_raw_scores = {
        dummy_users[2].line_user_id: 10000,
        dummy_users[3].line_user_id: 10000,
    }
    assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
    for k in expected_raw_scores:
        assert hanchans[0].raw_scores[k] == expected_raw_scores[k]


def test_execute_delete_last_one():
    # Arrange
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[1].line_user_id
    dummy_hanchan = Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[1].line_user_id: 10000,
        },
        converted_scores={},
        match_id=1,
        status=2,
        _id=1,
    )
    hanchan_repository.create(dummy_hanchan)
    dummy_match.active_hanchan_id = dummy_hanchan._id
    match_repository.create(dummy_match)
    group_repository.create(dummy_group)
    for dummy_user in dummy_users:
        user_repository.create(dummy_user)

    # Act
    use_case.execute(text='-')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == '点数を入力してください。'
    hanchans = hanchan_repository.find()
    expected_raw_scores = {}
    assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
    for k in expected_raw_scores:
        assert hanchans[0].raw_scores[k] == expected_raw_scores[k]
