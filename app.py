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

class METHOD(Enum):
    EXIT = 'exit'
    INPUT = 'input'
    MODE = 'mode'
    HELP = 'help'
    CALC = 'calculator'
    SETTING = 'settings'

MODE = Mode.WAIT
POINTS = []
SETTINGS = {'レート': '点3', '順位点': '0,0,0,0', '飛び賞': 'なし', 'チップ': 'なし'}

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
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    reply1 = f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は{profile.display_name}さんの快適な麻雀生活をサポートします。'
    # reply2 = f'今すぐ点数を計算したい場合は画面下のメニューを開き、[点数を入力する]を押してください(メニューがない場合は @INPUT と送信)'
    reply2 = f'今すぐ点数を計算したい場合は @INPUT と送信してください'
    reply3 = get_settings()

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=reply1), TextSendMessage(text=reply2), TextSendMessage(text=reply3)]
    )
    # rich_menu_id = create_start_menu()
    # line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
        
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    reply = routing_by_text(event)
    user_id = event.source.user_id
    logger.info('recieve text message')
    if not type(reply) == str:
        return
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))
    # rich_menu_id = create_start_menu()
    # line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)

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
        return input_point(text, event.source.user_id)

    return '雑談してる暇があったら麻雀の勉強をしましょう'

# route/text.method
def routing_by_method(method):
    if method == 'INPUT':
        reset_points()
        return change_mode('INPUT')
    elif method == 'CALC':
        return calculate()
    elif method == 'MODE':
        return get_mode()
    elif method == 'EXIT':
        return change_mode('WAIT')
    elif method == 'HELP':
        return 'まだ使い方書いてないからもうちょい待ってて'
    elif method == 'SETTING':
        return get_settings()
        
# services/calculate
def calculate():
    global POINTS
    if len(POINTS) != 4:
        return '四人分の点数を入力してください'
    if sum(POINTS) != 100000:
        return f'点数の合計が{sum(POINTS)}点です。合計100000点になるように修正してください。'
    calc_result = run_calculate()
    result = [f'{user+1}人目: {money}円' for user, money in enumerate(calc_result)]
    return "\n".join(result)

def run_calculate():
    global POINTS
    max_value = max(POINTS)
    max_index = POINTS.index(max_value)
    tmp = []
    for p in [p for p in POINTS if p != max_value]:
        tmp.append(int((p - 30000)/1000))
    tmp.insert(max_index, -1*sum(tmp))
    return [p*30 for p in tmp]

# services/input
def input_point(text, user_id):
    profile = line_bot_api.get_profile(user_id)
    target_user = profile.display_name
    # if text[0] == '@':
    #     point, target_user = get_point_with_target_user(text)
    # else:
    #     point = text
    point = text
    isMinus = False
    if point[0] == '-':
        point = point[1:]
        isMinus = True

    if point.isnumeric() == False:
        return '点数は整数で入力してください。全員分の点数入力を終えた場合は @CALC と送信してください。（中断したい場合は @EXIT)（同点はまだサポートできていませんのであしからず）'
    
    if isMinus == True:
        point = '-' + point
    
    point = int(point)
    add_point(point)
    return get_points()

def add_point(point):
    global POINTS
    POINTS.append(point)
    if len(POINTS) > 4:
        POINTS = POINTS[-4:]

def get_points():
    global POINTS

    result = [f'{target_user+1}人目: {text}点' for target_user, text in enumerate(POINTS)]
    return "\n".join(result)

def reset_points():
    global POINTS
    POINTS = []

# services/settings
def get_settings():
    global SETTINGS
    s = [f'{key}: {value}' for key, value in SETTINGS.items()]
    return '[設定]\n' + '\n'.join(s)
    
# services/mode
def change_mode(mode):
    global MODE
    if not mode in [e.name for e in Mode]:
        return '@HELPで使い方を参照できます'
    MODE = Mode[mode]
    if MODE == Mode.INPUT:
        return '点数を入力してください。四回以上入力された場合は最新の4つを採用します。'
    elif MODE == Mode.WAIT:
        return '今日のラッキー牌は「リャンピン」です'

def get_mode():
    global MODE
    return MODE.value

# services/rich_menu
def create_start_menu():
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="start menu",
        chat_bar_text="メニュー",
        areas=[
            RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
                    action=get_mode()
                )
            ]
        ) 
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    file_path = './images/rich/input.png'
    content_type = 'Image/png'
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
