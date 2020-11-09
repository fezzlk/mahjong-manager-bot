# import public libraries
import os, psycopg2, json, random
from enum import Enum
from flask import Flask, request, abort
from flask.logging import create_logger
from scipy.stats import rankdata
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
    OFF = 'off'
    DELETE = 'delete'

class METHOD(Enum):
    EXIT = 'exit'
    INPUT = 'input'
    MODE = 'mode'
    HELP = 'help'
    CALC = 'calculator'
    SETTING = 'settings'
    OFF = 'off'
    ON = 'on'
    RESET = 'reset'
    RESULTS = 'result'
    DELETE = 'delete'

MODE = Mode.WAIT
POINTS = {}
RESULTS = []
REPLIES = []
PRIZE = [30, 10, -10, -30]
SETTINGS = {'レート': '点3', '順位点': str(PRIZE), '飛び賞': 'なし', 'チップ': 'なし'}
KANSUJI = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
HAI = [k+'萬' for k in KANSUJI] + [k+'筒' for k in KANSUJI] + [k+'索' for k in KANSUJI] + ['白', '發', '中', '東', '南', '西', '北']

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
    global REPLIES
    REPLIES = []
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    add_reply(f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は{profile.display_name}さんの快適な麻雀生活をサポートします。')
    # add_reply(f'今すぐ点数を計算したい場合は画面下のメニューを開き、[点数を入力する]を押してください(メニューがない場合は @INPUT と送信)')
    add_reply(f'今すぐ点数を計算したい場合は @INPUT と送信してください')
    reply_settings()

    messages = []
    for reply in REPLIES:
        messages.append(TextSendMessage(text=reply))
    line_bot_api.reply_message(
        event.reply_token,
        messages)
    # rich_menu_id = create_start_menu()
    # line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
        
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global REPLIES
    REPLIES = []
    routing_by_text(event)
    user_id = event.source.user_id
    logger.info('recieve text message')
    messages = []
    for reply in REPLIES:
        messages.append(TextSendMessage(text=reply))
    line_bot_api.reply_message(
        event.reply_token,
        messages)
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
        routing_by_method(text[1:])
        return

    if MODE == Mode.INPUT:
        input_point(text, event.source.user_id)
        return
    
    if MODE == Mode.DELETE:
        if text.isdigit() == False:
            add_reply('数字で指定してください。')
            return
        i = int(text)
        if 0 < i & count_results <= i:
            drop_result(i-1)
            add_reply(f'{i}回目の結果を削除しました。')
            return
        add_reply('指定された結果が存在しません。')
        return

    add_reply('雑談してる暇があったら麻雀の勉強をしましょう')

# route/text.method
def routing_by_method(method):
    if method == 'INPUT':
        reset_points()
        change_mode('INPUT')
    elif method == 'CALC':
        calculate()
    elif method == 'MODE':
        reply_mode()
    elif method == 'EXIT':
        change_mode('WAIT')
    elif method == 'HELP':
        add_reply('まだ使い方書いてないからもうちょい待ってて')
        add_reply('\n'.join(['@' + e.name for e in METHOD]))
    elif method == 'SETTING':
        reply_settings()
    elif method == 'OFF':
        change_mode('OFF')
    elif method == 'ON':
        change_mode('WAIT')
    elif method == 'RESET':
        reset_results()
    elif method == 'RESULTS':
        reply_results()
    elif method == 'DELETE':
        change_mode('DELETE')

# services/reply
def add_reply(text):
    global REPLIES
    REPLIES.append(text)

# services/calculate
def calculate():
    global POINTS
    if len(POINTS) != 4:
        add_reply('四人分の点数を入力してください。点数を取り消したい場合は @{ユーザー名} と送ってください。')
        return
    if int(sum(POINTS.values())/1000) != 100:
        add_reply(f'点数の合計が{sum(POINTS.values())}点です。合計100000点+αになるように修正してください。')
        return
    calc_result = run_calculate()
    add_result(calc_result)
    reply_current_result()

def run_calculate():
    global POINTS, PRIZE

    sorted_points = sorted(POINTS.items(), key=lambda x:x[1])
    result = {}
    for t in sorted_points[:-1]:
        result[t[0]] = int(t[1]/1000) - 30
    result[sorted_points[-1][0]] = -1 * sum(result.values())
    sorted_prize = sorted(PRIZE)
    for i, t in enumerate(sorted_points):
        result[t[0]] = result[t[0]] + sorted_prize[i]
    return result

# services/input
def input_point(text, user_id):
    profile = line_bot_api.get_profile(user_id)
    target_user = profile.display_name
    if text[0] == '@':
        point, target_user = get_point_with_target_user(text[1:])
        if point == 'delete':
            drop_point(target_user)
            reply_points()
            return
    else:
        point = text
    isMinus = False
    if point[0] == '-':
        point = point[1:]
        isMinus = True

    if point.isnumeric() == False:
        add_reply('点数は整数で入力してください。全員分の点数入力を終えた場合は @CALC と送信してください。（中断したい場合は @EXIT)')
    
    if isMinus == True:
        point = '-' + point
    
    register_point(target_user, int(point))
    reply_points()

def get_point_with_target_user(text):
    s = text.split()
    if len(s) >= 2:
        return s[-1], ' '.join(s[:-1])
    elif len(s) == 1:
        return 'delete', s[0]

def register_point(name, point):
    global POINTS
    POINTS[name] = point

def drop_point(name):
    global POINTS
    if name in POINTS.keys():
        POINTS.pop(name)

def reply_points():
    global POINTS
    if len(POINTS) != 0:
        result = [f'{target_user}: {point}点' for target_user, point in POINTS.items()]
        add_reply("\n".join(result))
        return
    add_reply('点数を入力してください。ユーザーを指定したい場合は「@{ユーザー名) {点数}」と送ってください。')

def reset_points():
    global POINTS
    POINTS = {}

# services/settings
def reply_settings():
    global SETTINGS
    s = [f'{key}: {value}' for key, value in SETTINGS.items()]
    add_reply('[設定]\n' + '\n'.join(s))

# services/result
def add_result(result):
    global RESULTS
    RESULTS.append(result)

def drop_result(i):
    global RESULTS
    if len(RESULTS) > i:
        RESULTS.pop(i)

def reply_current_result():
    add_reply(f'一半荘お疲れ様でした。結果を表示します。')
    reply_result(count_results()-1)
    add_reply('今回の結果に一喜一憂せず次の戦いに望んでください。')

def reply_result(i):
    global RESULTS
    target = RESULTS[i]
    result = [f'{user}: {point}' for user, point in target.items()]
    add_reply(f'第{count_results()}回\n' + '\n'.join(result))

# services/results
def count_results():
    global RESULTS
    return len(RESULTS)

def reset_results():
    global RESULTS
    RESULTS = []
    add_reply('結果を全て削除しました。')

def reply_results():
    add_reply('これまでの対戦結果です。')
    for i in range(count_results()):
        reply_result(i)
    
# services/mode
def change_mode(mode):
    global MODE
    if not mode in [e.name for e in Mode]:
        add_reply('@HELPで使い方を参照できます')
        return
    MODE = Mode[mode]
    if MODE == Mode.INPUT:
        add_reply(f'第{count_results()+1}回戦お疲れ様です。各自点数を入力してください。（同点の場合は上家が高くなるように数点追加してください）全員分の点数入力を終えた場合は @CALC と送信してください。（中断したい場合は @EXIT)')
        return
    elif MODE == Mode.WAIT:
        add_reply(f'こんにちは。快適な麻雀生活の提供に努めます。今日のラッキー牌は「{get_random_hai()}」です。')
        return
    elif MODE == Mode.OFF:
        add_reply('会話に参加しないようにします。私を使いたい時は @ON と送信してください。')
        return
    elif MODE == Mode.DELETE:
        add_reply('削除したい結果を数字で指定してください。')
        reply_results()
        return

def get_random_hai():
    global HAI
    return random.choice(HAI)

def reply_mode():
    global MODE
    add_reply(MODE.value)

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
                    action=reply_mode()
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
