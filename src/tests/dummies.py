from typing import Dict, List
from DomainModel.entities.Config import Config
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Group import Group, GroupMode
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match

from line_models.Profile import Profile
from line_models.Event import Event


'''
    list 内の既存のインスタンスは変更禁止、追加のみ可能
    使用側では find_all などの特殊な場合を除いて [:3] などを使い追加に影響しないようにする
'''


def generate_dummy_config_list() -> List[Config]:
    users = generate_dummy_user_list()
    groups = generate_dummy_group_list()

    return [
        Config(
            target_id=users[0].line_user_id,
            key='飛び賞',
            value='30',
            _id=1,
        ),
        Config(
            target_id=users[0].line_user_id,
            key='レート',
            value='点2',
            _id=2,
        ),
        Config(
            target_id=users[1].line_user_id,
            key='飛び賞',
            value='20',
            _id=3,
        ),
        Config(
            target_id=groups[0].line_group_id,
            key='飛び賞',
            value='0',
            _id=4,
        ),
        Config(
            target_id=groups[0].line_group_id,
            key='レート',
            value='点2',
            _id=5,
        ),
        Config(
            target_id=groups[1].line_group_id,
            key='飛び賞',
            value='10',
            _id=6,
        ),
    ]


def generate_dummy_user_list() -> List[User]:
    return [
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
        # same line_user_name _id=3
        User(
            line_user_name="test_user3",
            line_user_id="U0123456789abcdefghijklmnopqrstu4",
            zoom_url="https://us00web.zoom.us/j/01234567894?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama_user4",
            matches=[],
            _id=4,
        ),
        User(
            line_user_name="test_user5",
            line_user_id="dummy_user_id",
            zoom_url="https://us00web.zoom.us/j/01234567895?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama_user5",
            matches=[],
            _id=5,
        ),
        User(
            line_user_name="test user6",
            line_user_id="dummy_user_id",
            zoom_url="https://us00web.zoom.us/j/01234567895?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user6",
            matches=[],
            _id=5,
        ),
    ]


def generate_dummy_group_list() -> List[Group]:
    return [
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            zoom_url="https://us01web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=GroupMode.wait,
            _id=1,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
            zoom_url="https://us01web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=GroupMode.wait,
            _id=2,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu3",
            zoom_url="https://us01web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=GroupMode.wait,
            _id=3,
        ),
        # same line group id 3
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu3",
            zoom_url="https://us01web.zoom.us/j/01234567894?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=GroupMode.input,
            _id=4,
        ),
    ]


def generate_dummy_hanchan_list() -> List[Hanchan]:
    groups = generate_dummy_group_list()
    users = generate_dummy_user_list()

    return [
        Hanchan(
            line_group_id=groups[0].line_group_id,
            raw_scores={},
            converted_scores={},
            match_id=1,
            status=1,
            _id=1,
        ),
        Hanchan(
            line_group_id=groups[0].line_group_id,
            raw_scores={},
            converted_scores={},
            match_id=1,
            status=2,
            _id=2,
        ),
        Hanchan(
            line_group_id=groups[0].line_group_id,
            raw_scores={},
            converted_scores={},
            match_id=1,
            status=0,
            _id=3,
        ),
        Hanchan(
            line_group_id=groups[0].line_group_id,
            raw_scores={},
            converted_scores={},
            match_id=2,
            status=1,
            _id=4,
        ),
        Hanchan(
            line_group_id=groups[1].line_group_id,
            raw_scores={},
            converted_scores={},
            match_id=5,
            status=1,
            # same the other's id
            _id=4,
        ),
        Hanchan(
            line_group_id=groups[0].line_group_id,
            raw_scores={
                users[0].line_user_id: 40000,
                users[1].line_user_id: 30000,
                users[2].line_user_id: 20000,
                users[3].line_user_id: 10000,
            },
            converted_scores={
                users[0].line_user_id: 50,
                users[1].line_user_id: 10,
                users[2].line_user_id: -20,
                users[3].line_user_id: -40,
            },
            match_id=1,
            status=1,
            _id=6,
        ),
        Hanchan(
            line_group_id=groups[0].line_group_id,
            raw_scores={
                users[0].line_user_id: 40000,
                users[1].line_user_id: 30000,
                users[2].line_user_id: 20000,
                users[4].line_user_id: 10000,
            },
            converted_scores={
                users[0].line_user_id: 50,
                users[1].line_user_id: 10,
                users[2].line_user_id: -20,
                users[4].line_user_id: -40,
            },
            match_id=1,
            status=1,
            _id=7,
        ),
    ]


def generate_dummy_match_list() -> List[Match]:
    groups = generate_dummy_group_list()

    return [
        Match(
            line_group_id=groups[0].line_group_id,
            hanchan_ids=[1, 2, 3, 6, 7],
            users=[],
            status=1,
            _id=1,
        ),
        Match(
            line_group_id=groups[0].line_group_id,
            hanchan_ids=[4],
            users=[],
            status=2,
            _id=2,
        ),
        Match(
            line_group_id=groups[0].line_group_id,
            hanchan_ids=[],
            users=[],
            status=0,
            _id=3,
        ),
        Match(
            line_group_id=groups[0].line_group_id,
            hanchan_ids=[],
            users=[],
            status=0,
            _id=4,
        ),
        Match(
            line_group_id=groups[1].line_group_id,
            hanchan_ids=[4],
            users=[],
            status=0,
            _id=5,
        ),
    ]


def generate_dummy_follow_event() -> Event:
    return Event(
        event_type='follow',
        source_type='user',
        user_id=generate_dummy_user_list()[0].line_user_id,
    )


def generate_dummy_unfollow_event() -> Event:
    return Event(
        event_type='unfollow',
        source_type='user',
        user_id=generate_dummy_user_list()[0].line_user_id,
    )


def generate_dummy_join_event() -> Event:
    return Event(
        event_type='join',
        source_type='group',
        user_id=generate_dummy_user_list()[0].line_user_id,
        group_id=generate_dummy_group_list()[0].line_group_id,
    )


def generate_dummy_text_message_event_from_user() -> Event:
    return Event(
        event_type='message',
        source_type='user',
        user_id=generate_dummy_user_list()[0].line_user_id,
        message_type='text',
        text='dummy_text',
    )


def generate_dummy_text_message_event_from_group() -> Event:
    return Event(
        event_type='message',
        source_type='group',
        user_id=generate_dummy_user_list()[0].line_user_id,
        group_id=generate_dummy_group_list()[0].line_group_id,
        message_type='text',
        text='dummy_text',
    )


def generate_dummy_profile() -> Profile:
    return Profile(
        display_name='dummy_display_name',
        user_id='dummy_user_id',
    )


def generate_dummy_points() -> Dict[str, int]:
    return {
        'dummy_user1': 10000,
        'dummy_user2': 20000,
        'dummy_user3': 30000,
        'dummy_user4': 40000,
    }
