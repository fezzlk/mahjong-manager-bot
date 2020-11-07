# import public libraries
import os, psycopg2, json
from enum import Enum
from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent,
    MessageEvent,
    TextMessage, 
    TextSendMessage,
    ImageMessage,
    RichMenu,
    RichMenuSize,
    RichMenuArea,
    RichMenuBounds,
    URIAction
)

# import original module
import local_env
local_env.set_env()

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__)
logger = create_logger(app)
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# define enums
class Mode(Enum):
    WAIT = 'wait'
    INPUT = 'input'
MODE = Mode.WAIT

class METHOD(Enum):
    EXIT = 'exit'
    INPUT = 'input'
    MODE = 'mode'
    HELP = 'help'

# server root
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# routing by message type
# follow
@handler.add(FollowEvent)
def handle_follow(event):
    reply = 'フォローありがとう'
    user_id = event.source.user_id
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))
    rich_menu_id = create_start_menu()
    line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
        
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    print(MODE)
    reply = routing_by_text(event)
    user_id = event.source.user_id
    logger.info('recieve text message')
    if not type(reply) == str:
        return
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))
    rich_menu_id = create_start_menu()
    line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    reply = 'not support image message'
    logger.info('recieve image message')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))

# route/text
def routing_by_text(event):
    global MODE
    text = event.message.text
    prefix = text[0]
    if (prefix == '@') & (text[1:] in [e.name for e in METHOD]):
        return routing_by_method(text[1:])

    if MODE == Mode.INPUT:
        return 'input mode now'

    return text

# route/text.method
def routing_by_method(method):
    if method == 'INPUT':
        return change_mode('INPUT')
    elif method == 'MODE':
        return get_mode()
    elif method == 'EXIT':
        return change_mode('WAIT')

# services/mode
def change_mode(mode):
    global MODE
    if not mode in [e.name for e in Mode]:
        return '@HELPで使い方を参照できます'
    MODE = Mode[mode]
    return f'set mode:{MODE.value}'

def get_mode():
    global MODE
    return MODE.value

# services/rich_menu
def create_start_menu():
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="Nice richmenu",
        chat_bar_text="Tap here",
        areas=[
            RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
                    action=URIAction(label='Go to line.me', uri='https://line.me')
                )
            ]
        ) 
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    file_path = './images/rich/2020093002.jpg'
    content_type = 'Image/jpeg'
    with open(file_path, 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)
    return rich_menu_id

# def get_connection():
#     return psycopg2.connect(DATABASE_URL, sslmode='require')

# def get_cursor():
#     with get_connection() as conn:
#         with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
#             return cur

# def post_user():
#     with get_cursor() as cur:
#         cur.execute()

if __name__ == "__main__":
   app.run()
    # port = int(os.getenv("PORT"))
    # app.run(host="0.0.0.0", port=port)
