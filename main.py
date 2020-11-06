from flask import Flask, request, abort
import os
import local_env
local_env.set_env()
import psycopg2
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
DATABASE_URL = os.environ['DATABASE_URL']

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

from enum import Enum
class Mode(Enum):
    WAIT = 'wait'
    INPUT = 'input'

mode = Mode.WAIT

@app.route("/")
def hello_world():
    return "hello world!"

def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def get_cursor():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            return cur

def post_user():
    with get_cursor() as cur:
        cur.execute()

def routing(message):
    m_type = message['type']
    if m_type == 'text':
        text = message['text']
        routing_by_text(text)
        return 'text'
    elif m_type == 'image':
        return 'image'
    else:
        return 'other'

def routing_by_text(text):
    return text

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    event = request.get_json()['events'][0]
    userId = event['source']['userId']
    message = event['message']
    result = routing(message)
    print(mode.value)
    # app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
   app.run()
    # port = int(os.getenv("PORT"))
    # app.run(host="0.0.0.0", port=port)
