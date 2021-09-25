from domains.Config import Config
from domains.User import User, UserMode
from domains.Room import Room, RoomMode
from domains.Hanchan import Hanchan
from domains.Match import Match


# list 内の既存のインスタンスは変更禁止、追加のみ可能
# 使用側では find_all などの特殊な場合を除いて [:3] などを使い追加に影響しないようにする


def generate_dummy_config():
    return generate_dummy_config_list()[0]


def generate_dummy_config_list():
    users = generate_dummy_user_list()
    rooms = generate_dummy_room_list()

    return [
        Config(
            target_id=users[0].line_user_id,
            key='飛び賞',
            value='10',
            _id=1,
        ),
        Config(
            target_id=users[0].line_user_id,
            key='レート',
            value='2',
            _id=2,
        ),
        Config(
            target_id=users[1].line_user_id,
            key='飛び賞',
            value='10',
            _id=3,
        ),
        Config(
            target_id=rooms[0].line_room_id,
            key='飛び賞',
            value='10',
            _id=4,
        ),
        Config(
            target_id=rooms[0].line_room_id,
            key='レート',
            value='2',
            _id=5,
        ),
        Config(
            target_id=rooms[1].line_room_id,
            key='飛び賞',
            value='10',
            _id=6,
        ),
    ]


def generate_dummy_user():
    return generate_dummy_user_list()[0]


def generate_dummy_user_list():
    return [
        User(
            name="test user1",
            line_user_id="U0123456789abcdefghijklmnopqrstu1",
            zoom_url="https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user1",
            matches=[],
            _id=1,
        ),
        User(
            name="test user2",
            line_user_id="U0123456789abcdefghijklmnopqrstu2",
            zoom_url="https://us00web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user2",
            matches=[],
            _id=2,
        ),
        User(
            name="test user3",
            line_user_id="U0123456789abcdefghijklmnopqrstu3",
            zoom_url="https://us00web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user3",
            matches=[],
            _id=3,
        ),
        # same name _id=3
        User(
            name="test user3",
            line_user_id="U0123456789abcdefghijklmnopqrstu4",
            zoom_url="https://us00web.zoom.us/j/01234567894?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user4",
            matches=[],
            _id=4,
        ),
    ]


def generate_dummy_room():
    return generate_dummy_room_list()[0]


def generate_dummy_room_list():
    return [
        Room(
            line_room_id="R0123456789abcdefghijklmnopqrstu1",
            zoom_url="https://us01web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=RoomMode.wait,
            _id=1,
        ),
        Room(
            line_room_id="R0123456789abcdefghijklmnopqrstu2",
            zoom_url="https://us01web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=RoomMode.wait,
            _id=2,
        ),
        Room(
            line_room_id="R0123456789abcdefghijklmnopqrstu3",
            zoom_url="https://us01web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=RoomMode.wait,
            _id=3,
        ),
    ]


def generate_dummy_hanchan():
    return generate_dummy_hanchan_list()[0]


def generate_dummy_hanchan_list():
    rooms = generate_dummy_room_list()
    
    return [
        Hanchan(
            line_room_id=rooms[0].line_room_id,
            raw_scores={},
            converted_scores={},
            match_id=1,
            status=1,
            _id=1,
        ),
        Hanchan(
            line_room_id=rooms[0].line_room_id,
            raw_scores={},
            converted_scores={},
            match_id=1,
            status=2,
            _id=2,
        ),
        Hanchan(
            line_room_id=rooms[0].line_room_id,
            raw_scores={},
            converted_scores={},
            match_id=1,
            status=0,
            _id=3,
        ),
        Hanchan(
            line_room_id=rooms[0].line_room_id,
            raw_scores={},
            converted_scores={},
            match_id=2,
            status=1,
            _id=4,
        ),
        Hanchan(
            line_room_id=rooms[1].line_room_id,
            raw_scores={},
            converted_scores={},
            match_id=5,
            status=1,
            # same the other's id
            _id=4,
        ),
    ]


def generate_dummy_match():
    return generate_dummy_match_list()[0]


def generate_dummy_match_list():
    rooms = generate_dummy_room_list()

    return [
        Match(
            line_room_id=rooms[0].line_room_id,
            hanchan_ids=[],
            users=[],
            status=1,
            _id=1,
        ),
        Match(
            line_room_id=rooms[0].line_room_id,
            hanchan_ids=[],
            users=[],
            status=2,
            _id=2,
        ),
        Match(
            line_room_id=rooms[0].line_room_id,
            hanchan_ids=[],
            users=[],
            status=0,
            _id=3,
        ),
        Match(
            line_room_id=rooms[0].line_room_id,
            hanchan_ids=[],
            users=[],
            status=0,
            _id=4,
        ),
        Match(
            line_room_id=rooms[1].line_room_id,
            hanchan_ids=[],
            users=[],
            status=0,
            _id=5,
        ),
    ]


def generate_dummy_request():
    return generate_dummy_match_list()[0]


def generate_dummy_follow_event():
    return Event(
        event_type='follow',
        source_type='user',
        user_id=generate_dummy_user().line_user_id,
    )


def generate_dummy_text_message_event_from_user():
    return Event(
        event_type='message',
        source_type='user',
        user_id=generate_dummy_user().line_user_id,
        message_type='text',
        text='dummy_text',
    )


def generate_dummy_text_message_event_from_room():
    return Event(
        event_type='message',
        source_type='room',
        user_id=generate_dummy_user().line_user_id,
        room_id=generate_dummy_room().line_room_id,
        message_type='text',
        text='dummy_text',
    )


# LINE messaging API に合わせるためフィールド名はキャメルケースにしている
class Event:
    def __init__(
        self,
        event_type='message',
        source_type='user',
        user_id=generate_dummy_user().line_user_id,
        room_id=generate_dummy_room().line_room_id,
        message_type='text',
        text='dummy_text',
        postback_data='dummy_postback_data',
        mode='active',
    ):
        self.type = event_type
        self.replyToken = 'dummy_reply_token'
        self.source = Source(user_id=user_id, source_type=source_type, room_id=room_id)
        self.mode = mode
        if self.type == 'message':
            self.message = Message(text=text, message_type=message_type)
        if self.type == 'postback':
            self.postback == Postback(data=postback_data)


class Source:
    def __init__(
        self,
        user_id=generate_dummy_user().line_user_id,
        source_type='user',
        room_id=generate_dummy_room().line_room_id,
    ):
        self.type = source_type
        self.user_id = user_id

        if source_type == 'room':
            dummy_room = generate_dummy_room()
            self.room_id = dummy_room.line_room_id


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
