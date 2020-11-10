from enum import Enum

class Methods(Enum):
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
    FINISH = 'finish'

from services import (
    AppService,
    CalculateService,
    ConfigService,
    ModeService,
    PointsService,
    ReplyService,
    ResultsService,
    RichMenuService,
)

app_service = AppService()
line_bot_api = app_service.line_bot_api

reply_service = ReplyService(line_bot_api)
config_service = ConfigService(reply_service)
points_service = PointsService(app_service, reply_service, config_service)
calculate_service = CalculateService(reply_service, points_service, config_service)
results_service = ResultsService(reply_service, points_service, config_service)
mode_service = ModeService(app_service, reply_service, results_service, points_service)
rich_menu_service = RichMenuService(app_service)

### routes/event
def follow(event):
    reply_service.reset()
    app_service.req_user_id = event.source.user_id
    profile = line_bot_api.get_profile(app_service.req_user_id)
    reply_service.add(f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は{profile.display_name}さんの快適な麻雀生活をサポートします。')
    reply_service.reply(event)
    rich_menu_service.create_and_link('personal')

def textMessage(event):
    reply_service.reset()
    routing_by_text(event)
    reply_service.reply(event)

def imageMessage(event):
    reply_service.reset()
    reply_service.add('画像への返信はまだサポートされていません。開発者に寄付をすれば対応を急ぎます。')
    reply_service.reply(event)

def postback(event):
    app_service.req_user_id = event.source.user_id
    reply_token = event.reply_token
    postback_msg = event.postback.data
    print(postback_msg)

### routes/text
def routing_by_text(event):
    text = event.message.text
    prefix = text[0]
    if (prefix == '@') & (text[1:] in [e.name for e in Methods]):
        routing_by_method(text[1:])
        return

    if mode_service.mode == mode_service.modes.INPUT:
        points_service.add_by_text(text)
        return
    
    if mode_service.mode == mode_service.modes.DELETE:
        if text.isdigit() == False:
            reply_service.add('数字で指定してください。')
            return
        i = int(text)
        if 0 < i & results_service.count() <= i:
            results_service.drop(i-1)
            reply_service.add(f'{i}回目の結果を削除しました。')
            return
        reply_service.add('指定された結果が存在しません。')
        return

    reply_service.add('雑談してる暇があったら麻雀の勉強をしましょう')

# routes/text.method
def routing_by_method(method):
    if method == Methods.INPUT.name:
        points_service.reset()
        mode_service.update(mode_service.modes.INPUT)
    elif method == Methods.CALC.name:
        calculate_service.calculate()
    elif method == Methods.MODE.name:
        mode_service.reply()
    elif method == Methods.EXIT.name:
        mode_service.update(mode_service.modes.WAIT)
    elif method == Methods.HELP.name:
        reply_service.add('まだ使い方書いてないからもうちょい待ってて')
        reply_service.add('\n'.join(['@' + e.name for e in Methods]))
    elif method == Methods.SETTING.name:
        config_service.reply()
    elif method == Methods.OFF.name:
        mode_service.update(mode_service.modes.OFF)
    elif method == Methods.ON.name:
        mode_service.update(mode_service.modes.WAIT)
    elif method == Methods.RESET.name:
        results_service.reset()
    elif method == Methods.RESULTS.name:
        results_service.reply()
    elif method == Methods.DELETE.name:
        mode_service.update(mode_service.modes.DELETE)
    elif method == Methods.FINISH.name:
        results_service.reply_sum_and_money()

