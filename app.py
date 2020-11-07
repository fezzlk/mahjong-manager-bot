# import public libraries
import os, psycopg2
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
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
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
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # json = request.get_json()
    # result = ''
    # if len(json['events']) >= 1:
    #     result = control(json['events'][0])
    print(event)
    print(event.message.text)
    logger.info('recieve text message')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    logger.info('recieve image message')
    return


def routing_by_type(message):
    m_type = message['type']
    if m_type == 'text':
        text = message['text']
        return routing_by_text(text)
    elif m_type == 'image':
        return 'image'
    else:
        return 'other'

def routing_by_text(text):
    prefix = text[0]
    if prefix == '@':
        return change_mode(text)
    else:
        return text

def change_mode(text):
    MODE = Mode[text[1:]]
    return f'set mode:{MODE.value}'    

def control(event):
    userId = event['source']['userId']
    message = event['message']
    if MODE == Mode.WAIT:
        return routing_by_type(message)
    elif MODE == Mode.INPUT:
        return 'input mode now'


@app.route("/")
def hello_world():
    return "hello world!"

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
