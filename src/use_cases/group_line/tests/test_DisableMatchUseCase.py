from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Group import Group, GroupMode
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from use_cases.group_line.DisableMatchUseCase import DisableMatchUseCase
from ApplicationService import (
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
    ),
    User(
        line_user_name="test_user2",
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        zoom_url="https://us00web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user2",
        matches=[],
    ),
    User(
        line_user_name="test_user3",
        line_user_id="U0123456789abcdefghijklmnopqrstu3",
        zoom_url="https://us00web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user3",
        matches=[],
    ),
    User(
        line_user_name="test_user4",
        line_user_id="U0123456789abcdefghijklmnopqrstu4",
        zoom_url="https://us00web.zoom.us/j/01234567894?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user4",
        matches=[],
    ),
    User(
        line_user_name="test_user5",
        line_user_id="U0123456789abcdefghijklmnopqrstu5",
        zoom_url="https://us00web.zoom.us/j/01234567895?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=UserMode.wait,
        jantama_name="jantama_user5",
        matches=[],
    ),
]

dummy_hanchans = [
    Hanchan(
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[1].line_user_id: 10000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 30000,
            dummy_users[4].line_user_id: 40000,
        },
        converted_scores={
            dummy_users[1].line_user_id: -40,
            dummy_users[2].line_user_id: -20,
            dummy_users[3].line_user_id: 10,
            dummy_users[4].line_user_id: 50,
        },
        match_id=1,
        status=2,
    ),
    Hanchan(  # 新規追加
        line_group_id=dummy_group.line_group_id,
        raw_scores={
            dummy_users[0].line_user_id: 10000,
            dummy_users[2].line_user_id: 20000,
            dummy_users[3].line_user_id: 30000,
            dummy_users[4].line_user_id: 40000,
        },
        converted_scores={
            dummy_users[0].line_user_id: -40,
            dummy_users[2].line_user_id: -20,
            dummy_users[3].line_user_id: 10,
            dummy_users[4].line_user_id: 50,
        },
        match_id=1,
        status=2,
    ),
]


dummy_matches = [
    Match(
        line_group_id=dummy_group.line_group_id,
        hanchan_ids=[1, 2],
        users=[],
        status=1,
    ),
    Match(
        line_group_id=dummy_group.line_group_id,
        hanchan_ids=[1, 2],
        users=[],
        status=2,
    ),
]


def test_execute():
    # Arrange
    use_case = DisableMatchUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    request_info_service.req_line_user_id = dummy_users[0].line_user_id
    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(session, dummy_user)
        group_repository.create(session, dummy_group)
        match_repository.create(session, dummy_matches[0])
        for dummy_hanchan in dummy_hanchans:
            hanchan_repository.create(session, dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    with session_scope() as session:
        matches = match_repository.find_all(session)
        assert matches[0].status == 0
