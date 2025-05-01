from datetime import datetime
from typing import Dict, List

from bson.objectid import ObjectId

from DomainModel.entities.Group import Group, GroupMode
from DomainModel.entities.GroupSetting import GroupSetting
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.WebUser import WebUser
from line_models.Event import Event
from line_models.Profile import Profile

"""
    list 内の既存のインスタンスは変更禁止、追加のみ可能
    使用側では find などの特殊な場合を除いて [:3] などを使い追加に影響しないようにする
"""


def generate_dummy_user_list() -> List[User]:
    return [
        User(
            line_user_name="test_user1",
            line_user_id="U0123456789abcdefghijklmnopqrstu1",
            mode=UserMode.wait.value,
            jantama_name="jantama_user1",
        ),
        User(
            line_user_name="test_user2",
            line_user_id="U0123456789abcdefghijklmnopqrstu2",
            mode=UserMode.wait.value,
            jantama_name="jantama_user2",
        ),
        User(
            line_user_name="test_user3",
            line_user_id="U0123456789abcdefghijklmnopqrstu3",
            mode=UserMode.wait.value,
            jantama_name="jantama_user3",
        ),
        User(
            line_user_name="test_user4",
            line_user_id="U0123456789abcdefghijklmnopqrstu4",
            mode=UserMode.wait.value,
            jantama_name="jantama_user4",
        ),
        User(
            line_user_name="test_user5",
            line_user_id="U0123456789abcdefghijklmnopqrstu5",
            mode=UserMode.wait.value,
            jantama_name="jantama_user5",
        ),
        User(
            line_user_name="test user6",
            line_user_id="U0123456789abcdefghijklmnopqrstu6",
            mode=UserMode.wait.value,
            jantama_name="jantama_user6",
        ),
        User(
            line_user_name="test_user7",
            line_user_id="U0123456789abcdefghijklmnopqrstu7",
            mode=UserMode.wait.value,
            jantama_name="jantama_user7",
        ),
        User(
            line_user_name="test_user8",
            line_user_id="U0123456789abcdefghijklmnopqrstu8",
            mode=UserMode.wait.value,
            jantama_name="jantama_user8",
        ),
        User(
            line_user_name="test_user9",
            line_user_id="U0123456789abcdefghijklmnopqrstu9",
            mode=UserMode.wait.value,
            jantama_name="jantama_user9",
        ),
        User(
            line_user_id="U0123456789abcdefghijklmnopqrstu10",
        ),
    ]


def generate_dummy_web_user_list() -> List[WebUser]:
    return [
        WebUser(
            user_code="code1",
            name="name1",
            email="email1",
            linked_line_user_id=None,
            is_approved_line_user=False,
            created_at=datetime(2022, 1, 1, 12, 0, 0),
            updated_at=datetime(2022, 1, 1, 12, 0, 0),
        ),
        WebUser(
            user_code="code2",
            name="name2",
            email="email2",
            linked_line_user_id=None,
            is_approved_line_user=False,
            created_at=datetime(2022, 1, 1, 12, 0, 0),
            updated_at=datetime(2022, 1, 1, 12, 0, 0),
        ),
        WebUser(
            user_code="code3",
            name="name3",
            email="email3",
            linked_line_user_id=None,
            is_approved_line_user=False,
            created_at=datetime(2022, 1, 1, 12, 0, 0),
            updated_at=datetime(2022, 1, 1, 12, 0, 0),
        ),
        WebUser(
            user_code="code4",
        ),
    ]


def generate_dummy_group_list() -> List[Group]:
    return [
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            mode=GroupMode.wait.value,
            active_match_id=ObjectId("644c838186bbd9e20a91b785"),
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
            mode=GroupMode.wait.value,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu3",
            mode=GroupMode.wait.value,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu4",
            mode=GroupMode.wait.value,
        ),
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu5",
        ),
    ]


def generate_dummy_group_setting_list() -> List[GroupSetting]:
    return [
        GroupSetting(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            rate=3,
            ranking_prize=[20, 10, -10, -20],
            tip_rate=0,
            tobi_prize=10,
            num_of_players=4,
            rounding_method=0,
        ),
        GroupSetting(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
            rate=3,
            ranking_prize=[30, 10, -10, -30],
            tip_rate=0,
            tobi_prize=10,
            num_of_players=4,
            rounding_method=0,
        ),
        GroupSetting(
            line_group_id="G0123456789abcdefghijklmnopqrstu3",
        ),
        GroupSetting(
            line_group_id="G0123456789abcdefghijklmnopqrstu4",
        ),
        GroupSetting(
            line_group_id="G0123456789abcdefghijklmnopqrstu5",
        ),
    ]


def generate_dummy_match_list() -> List[Match]:
    groups = generate_dummy_group_list()

    return [
        Match(
            line_group_id=groups[0].line_group_id,
            status=2,
            _id=ObjectId("644c838186bbd9e20a91b783"),
        ),
        Match(
            line_group_id=groups[0].line_group_id,
            status=0,
            _id=ObjectId("644c838186bbd9e20a91b784"),
        ),
        Match(
            line_group_id=groups[0].line_group_id,
            status=2,
            active_hanchan_id=ObjectId("644c838186bbd9e20a91b784"),
            _id=ObjectId("644c838186bbd9e20a91b785"),
        ),
    ]


def generate_dummy_hanchan_list() -> List[Hanchan]:
    groups = generate_dummy_group_list()

    return [
        Hanchan(
            line_group_id=groups[0].line_group_id,
            match_id=ObjectId("644c838186bbd9e20a91b785"),
            status=2,
        ),
        Hanchan(
            line_group_id=groups[2].line_group_id,
            raw_scores={},
            converted_scores={},
            match_id=ObjectId("644c838186bbd9e20a91b785"),
            status=0,
        ),
        Hanchan(
            line_group_id=groups[2].line_group_id,
            raw_scores={},
            converted_scores={},
            match_id=ObjectId("644c838186bbd9e20a91b785"),
            status=2,
        ),
    ]


def generate_dummy_follow_event() -> Event:
    return Event(
        type="follow",
        source_type="user",
        user_id=generate_dummy_user_list()[0].line_user_id,
    )


def generate_dummy_unfollow_event() -> Event:
    return Event(
        type="unfollow",
        source_type="user",
        user_id=generate_dummy_user_list()[0].line_user_id,
    )


def generate_dummy_join_event() -> Event:
    return Event(
        type="join",
        source_type="group",
        user_id=generate_dummy_user_list()[0].line_user_id,
        group_id=generate_dummy_group_list()[0].line_group_id,
    )


def generate_dummy_text_message_event_from_user() -> Event:
    return Event(
        type="message",
        source_type="user",
        user_id=generate_dummy_user_list()[0].line_user_id,
        message_type="text",
        text="dummy_text",
    )


def generate_dummy_text_message_event_from_group() -> Event:
    return Event(
        type="message",
        source_type="group",
        user_id=generate_dummy_user_list()[0].line_user_id,
        group_id=generate_dummy_group_list()[0].line_group_id,
        message_type="text",
        text="dummy_text",
    )


def generate_dummy_profile() -> Profile:
    return Profile(
        display_name="dummy_display_name",
        user_id="dummy_user_id",
    )


def generate_dummy_points() -> Dict[str, int]:
    return {
        "dummy_user1": 10000,
        "dummy_user2": 20000,
        "dummy_user3": 30000,
        "dummy_user4": 40000,
    }
