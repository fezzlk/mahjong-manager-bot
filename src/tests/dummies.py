from abc import ABCMeta, abstractmethod
from typing import Dict, List
from Domains.Entities.Config import Config
from Domains.Entities.User import User, UserMode
from Domains.Entities.Group import Group, GroupMode
from Domains.Entities.Hanchan import Hanchan
from Domains.Entities.Match import Match


class IEvent(metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self,
        event_type: str,
        source_type: str,
        user_id: str,
        group_id: str,
        message_type: str,
        text: str,
        postback_data: str,
        mode: str,
    ):
        pass


class IProfile(metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self,
        display_name: str,
        user_id: str,
    ):
        pass


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
            value='40',
            _id=6,
        ),
    ]


def generate_dummy_user_list() -> List[User]:
    return [
        User(
            line_user_name="test user1",
            line_user_id="U0123456789abcdefghijklmnopqrstu1",
            zoom_url="https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user1",
            matches=[],
            _id=1,
        ),
        User(
            line_user_name="test user2",
            line_user_id="U0123456789abcdefghijklmnopqrstu2",
            zoom_url="https://us00web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user2",
            matches=[],
            _id=2,
        ),
        User(
            line_user_name="test user3",
            line_user_id="U0123456789abcdefghijklmnopqrstu3",
            zoom_url="https://us00web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user3",
            matches=[],
            _id=3,
        ),
        # same line_user_name _id=3
        User(
            line_user_name="test user3",
            line_user_id="U0123456789abcdefghijklmnopqrstu4",
            zoom_url="https://us00web.zoom.us/j/01234567894?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user4",
            matches=[],
            _id=4,
        ),
        User(
            line_user_name="test user5",
            line_user_id="dummy_user_id",
            zoom_url="https://us00web.zoom.us/j/01234567895?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user5",
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
    ]


def generate_dummy_match_list() -> List[Match]:
    groups = generate_dummy_group_list()

    return [
        Match(
            line_group_id=groups[0].line_group_id,
            hanchan_ids=[],
            users=[],
            status=1,
            _id=1,
        ),
        Match(
            line_group_id=groups[0].line_group_id,
            hanchan_ids=[],
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
            hanchan_ids=[],
            users=[],
            status=0,
            _id=5,
        ),
    ]


def generate_dummy_follow_event() -> IEvent:
    return Event(
        event_type='follow',
        source_type='user',
        user_id=generate_dummy_user_list()[0].line_user_id,
    )


def generate_dummy_unfollow_event() -> IEvent:
    return Event(
        event_type='unfollow',
        source_type='user',
        user_id=generate_dummy_user_list()[0].line_user_id,
    )


def generate_dummy_join_event() -> IEvent:
    return Event(
        event_type='join',
        source_type='group',
        user_id=generate_dummy_user_list()[0].line_user_id,
        group_id=generate_dummy_group_list()[0].line_group_id,
    )


def generate_dummy_text_message_event_from_user() -> IEvent:
    return Event(
        event_type='message',
        source_type='user',
        user_id=generate_dummy_user_list()[0].line_user_id,
        message_type='text',
        text='dummy_text',
    )


def generate_dummy_text_message_event_from_group() -> IEvent:
    return Event(
        event_type='message',
        source_type='group',
        user_id=generate_dummy_user_list()[0].line_user_id,
        group_id=generate_dummy_group_list()[0].line_group_id,
        message_type='text',
        text='dummy_text',
    )


def generate_dummy_profile() -> IProfile:
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


# LINE messaging API に合わせるためフィールド名はキャメルケースにしている
class Profile(IProfile):
    def __init__(
        self,
        display_name='dummy_display_name',
        user_id='dummy_user_id'
    ):
        self.display_name = display_name
        self.user_id = user_id


class Event(IEvent):
    def __init__(
        self,
        event_type='message',
        source_type='user',
        user_id=generate_dummy_user_list()[0].line_user_id,
        group_id=generate_dummy_group_list()[0].line_group_id,
        message_type='text',
        text='dummy_text',
        postback_data='dummy_postback_data',
        mode='active',
    ):
        self.type = event_type
        self.replyToken = 'dummy_reply_token'
        self.source = Source(
            user_id=user_id,
            source_type=source_type,
            group_id=group_id)
        self.mode = mode
        if self.type == 'message':
            self.message = Message(text=text, message_type=message_type)
        if self.type == 'postback':
            self.postback == Postback(data=postback_data)


class Source:
    def __init__(
        self,
        user_id=generate_dummy_user_list()[0].line_user_id,
        source_type='user',
        group_id=generate_dummy_group_list()[0].line_group_id,
    ):
        self.type = source_type
        self.user_id = user_id

        if source_type == 'group':
            self.group_id = group_id


class Message:
    def __init__(self, text='dummy_text', message_type='text'):
        self.type = message_type
        self.id = 'dummy_message_id'

        if message_type == 'image':
            self.contentProvider = {'type': 'line'}
        elif message_type == 'text':
            self.text = text


class Postback:
    def __init__(self, data=''):
        self.data = data
