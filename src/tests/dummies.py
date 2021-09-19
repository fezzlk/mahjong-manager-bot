from domains.config import Config
from domains.user import User, UserMode
from domains.room import Room, RoomMode


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
        ),
        Config(
            target_id=users[0].line_user_id,
            key='レート',
            value='2',
        ),
        Config(
            target_id=users[1].line_user_id,
            key='飛び賞',
            value='10',
        ),
        Config(
            target_id=rooms[0].line_room_id,
            key='飛び賞',
            value='10',
        ),
        Config(
            target_id=rooms[0].line_room_id,
            key='レート',
            value='2',
        ),
        Config(
            target_id=rooms[1].line_room_id,
            key='飛び賞',
            value='10',
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
        ),
        User(
            name="test user2",
            line_user_id="U0123456789abcdefghijklmnopqrstu2",
            zoom_url="https://us00web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user2",
            matches=[],
        ),
        User(
            name="test user3",
            line_user_id="U0123456789abcdefghijklmnopqrstu3",
            zoom_url="https://us00web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=UserMode.wait,
            jantama_name="jantama user3",
            matches=[],
        ),
    ]


def generate_dummy_room():
    return generate_dummy_room_list()[0]


def generate_dummy_room_list():
    return [
        Room(
            line_room_id="R0123456789abcdefghijklmnopqrstu1",
            zoom_url="https://us01web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=RoomMode,
            users=[],
        ),
        Room(
            line_room_id="R0123456789abcdefghijklmnopqrstu2",
            zoom_url="https://us01web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=RoomMode,
            users=[],
        ),
        Room(
            line_room_id="R0123456789abcdefghijklmnopqrstu3",
            zoom_url="https://us01web.zoom.us/j/01234567893?pwd=abcdefghijklmnopqrstuvwxyz",
            mode=RoomMode,
            users=[],
        ),
    ]