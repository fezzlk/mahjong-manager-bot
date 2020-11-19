from enum import Enum

class Methods(Enum):
    exit = 'exit'
    input = 'input'
    mode = 'mode'
    help = 'help'
    calc = 'calculator'
    setting = 'settings'
    off = 'off'
    on = 'on'
    reset = 'reset'
    results = 'results'
    delete = 'delete'
    finish = 'finish'
    github = 'github'

from services import Services
services = Services()

### routes/event
def follow(event):
    services.app_service.req_user_id = event.source.user_id
    profile = services.app_service.line_bot_api.get_profile(services.app_service.req_user_id)
    services.reply_service.add_text(f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は{profile.display_name}さんの快適な麻雀生活をサポートします。')
    services.reply_service.reply(event)
    services.rich_menu_service.create_and_link('personal')

def join(event):
    services.reply_service.add_text(f'こんにちは、今日は麻雀日和ですね。\n参加メンバーを登録をします。(編集したい場合は_members)')
    # services.members_service.init(event)
    services.reply_service.reply(event)

def textMessage(event):
    services.app_service.req_user_id = event.source.user_id
    routing_by_text(event)
    services.reply_service.reply(event)

def imageMessage(event):
    services.app_service.req_user_id = event.source.user_id
    services.reply_service.add_text('画像への返信はまだサポートされていません。開発者に寄付をすれば対応を急ぎます。')
    services.reply_service.reply(event)

def postback(event):
    services.app_service.req_user_id = event.source.user_id
    method = event.postback.data[1:]
    routing_by_method(method)
    services.reply_service.reply(event)

### routes/text
def routing_by_text(event):
    text = event.message.text
    prefix = text[0]
    if (prefix == '_') & (text[1:] in [e.name for e in Methods]):
        routing_by_method(text[1:])
        return

    if services.mode_service.mode == services.mode_service.modes.input:
        services.points_service.add_by_text(text)
        return
    
    if services.mode_service.mode == services.mode_service.modes.delete:
        if text.isdigit() == False:
            services.reply_service.add_text('数字で指定してください。')
            return
        i = int(text)
        if 0 < i & services.results_service.count() <= i:
            services.results_service.drop(i-1)
            services.reply_service.add_text(f'{i}回目の結果を削除しました。')
            return
        services.reply_service.add_text('指定された結果が存在しません。')
        return

    if prefix == '_':
        services.reply_service.add_text('使い方がわからない場合はメニューの中の「使い方」を押してください。')
        return
    services.reply_service.add_text('雑談してる暇があったら麻雀の勉強をしましょう')

# routes/text.method
def routing_by_method(method):
    # input
    if method == Methods.input.name:
        services.points_service.reset()
        services.mode_service.update(services.mode_service.modes.input)
    # calculate
    elif method == Methods.calc.name:
        services.calculate_service.calculate(services.points_service.points)
    # mode
    elif method == Methods.mode.name:
        services.mode_service.reply()
    # exit
    elif method == Methods.exit.name:
        services.mode_service.update(services.mode_service.modes.wait)
    # help
    elif method == Methods.help.name:
        services.reply_service.add_text('使い方は明日書きます。')
        services.reply_service.add_text('\n'.join(['_' + e.name for e in Methods]))
    # setting
    elif method == Methods.setting.name:
        services.config_service.reply()
    # off
    elif method == Methods.off.name:
        services.mode_service.update(services.mode_service.modes.off)
    # on
    elif method == Methods.on.name:
        services.mode_service.update(services.mode_service.modes.wait)
    # reset
    elif method == Methods.reset.name:
        services.results_service.reset()
    # results
    elif method == Methods.results.name:
        services.results_service.reply_all()
    # delete
    elif method == Methods.delete.name:
        services.mode_service.update(services.mode_service.modes.delete)
    # finish
    elif method == Methods.finish.name:
        services.results_service.finish()
    # github
    elif method == Methods.github.name:
        services.reply_service.add_text('https://github.com/bbladr/mahjong-manager-bot')