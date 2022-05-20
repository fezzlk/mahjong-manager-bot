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
    session_scope,
)

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    zoom_url="https://us01web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
    mode=GroupMode.input,
    _id=1,
)

dummy_users = [
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        zoom_url="https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user1",
        matches=[],
        _id=1,
    ),
    User(
        line_user_name="test_user2",
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        zoom_url="https://us00web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user2",
        matches=[],
        _id=2,
    ),
    User(
        line_user_name="test_user3",
        line_user_id="U0123456789abcdefghijklmnopqrstu3",
        zoom_url="https://us00web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user3",
        matches=[],
        _id=3,
    ),
    User(
        line_user_name="test_user4",
        line_user_id="U0123456789abcdefghijklmnopqrstu4",
        zoom_url="https://us00web.zoom.us/j/01234567894?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user4",
        matches=[],
        _id=4,
    ),
    User(
        line_user_name="test_user5",
        line_user_id="U0123456789abcdefghijklmnopqrstu5",
        zoom_url="https://us00web.zoom.us/j/01234567895?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user5",
        matches=[],
        _id=4,
    ),
]

dummy_hanchans = [
    Hanchan(  # 新規追加
        line_group_id=dummy_group.line_group_id,
        raw_scores={},
        converted_scores={},
        match_id=1,
        status=1,
        _id=1,
    ),
    Hanchan(  # 更新
        line_group_id=dummy_group.line_group_id,
        raw_scores={dummy_users[0].line_user_id: 2000},
        converted_scores={},
        match_id=1,
        status=1,
        _id=2,
    ),
    Hanchan(  # 別ユーザー新規追加
        line_group_id=dummy_group.line_group_id,
        raw_scores={dummy_users[1].line_user_id: 2000},
        converted_scores={},
        match_id=1,
        status=1,
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
        status=1,
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
        status=1,
        _id=1,
    ),
]


dummy_match = Match(
    line_group_id=dummy_group.line_group_id,
    hanchan_ids=[],
    users=[],
    status=1,
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
    # Arrage
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    with session_scope() as session:
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_hanchans[case1[0]])
        group_repository.create(session, dummy_group)
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)

    # Act
    use_case.execute(text=case1[1])

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == case1[2]
    with session_scope() as session:
        hanchans = hanchan_repository.find_all(session)
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
    # Arrage
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    with session_scope() as session:
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_hanchans[0])
        group_repository.create(session, dummy_group)
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)

    # Act
    use_case.execute(text=case2)

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == '点数は整数で入力してください。'
    with session_scope() as session:
        hanchans = hanchan_repository.find_all(session)
        expected_raw_scores = dummy_hanchans[0].raw_scores
        assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
        for k in expected_raw_scores:
            assert hanchans[0].raw_scores[k] == expected_raw_scores[k]


def test_execute_with_mention():
    # Arrage
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.mention_line_ids = [
        'U0123456789abcdefghijklmnopqrstu1']
    with session_scope() as session:
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_hanchans[0])
        group_repository.create(session, dummy_group)
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)

    # Act
    use_case.execute(text='@test_user1 1000')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == 'test_user1: 1000'
    with session_scope() as session:
        hanchans = hanchan_repository.find_all(session)
        expected_raw_scores = {'U0123456789abcdefghijklmnopqrstu1': 1000}
        assert len(hanchans[0].raw_scores) == len(expected_raw_scores)
        for k in expected_raw_scores:
            assert hanchans[0].raw_scores[k] == expected_raw_scores[k]


def test_execute_multi_mentions():
    # Arrage
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.mention_line_ids = [
        'U0123456789abcdefghijklmnopqrstu1',
        'U0123456789abcdefghijklmnopqrstu2',
    ]
    with session_scope() as session:
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_hanchans[0])
        group_repository.create(session, dummy_group)
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)

    # Act
    use_case.execute(text='@dummy1 @dummy2 1000')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == 'ユーザーを指定する場合はメンションをつけてメッセージの末尾に点数を入力してください。1回につき1人を指定するようにしてください。'
    with session_scope() as session:
        hanchans = hanchan_repository.find_all(session)
        assert len(hanchans[0].raw_scores) == 0


def test_execute_not_registered_user():
    # Arrage
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    request_info_service.mention_line_ids = ['dummy_line_id']
    with session_scope() as session:
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_hanchans[0])
        group_repository.create(session, dummy_group)
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)

    # Act
    use_case.execute(text='@dummy 1000')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == '友達登録していないユーザーは登録できません。'
    with session_scope() as session:
        hanchans = hanchan_repository.find_all(session)
        assert len(hanchans[0].raw_scores) == 0


def test_execute_fourth_input():
    # Arrage
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    with session_scope() as session:
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_hanchans[3])
        group_repository.create(session, dummy_group)
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)

    # Act
    use_case.execute(text='10000')

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == 'test_user2: 10000\ntest_user3: 10000\ntest_user4: 10000\ntest_user1: 10000'
    assert reply_service.texts[1].type == 'text'
    assert reply_service.texts[1].text == '点数の合計が40000点です。合計100000点+αになるように修正してください。'
    with session_scope() as session:
        hanchans = hanchan_repository.find_all(session)
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
    # Arrage
    use_case = AddPointByTextUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    with session_scope() as session:
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_hanchans[4])
        group_repository.create(session, dummy_group)
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)

    # Act
    use_case.execute(text='10000')

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == 'test_user2: 10000\ntest_user3: 10000\ntest_user4: 10000\ntest_user5: 10000\ntest_user1: 10000'
    assert reply_service.texts[1].type == 'text'
    assert reply_service.texts[1].text == '5人以上入力されています。@[ユーザー名] で不要な入力を消してください。'
    with session_scope() as session:
        hanchans = hanchan_repository.find_all(session)
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
