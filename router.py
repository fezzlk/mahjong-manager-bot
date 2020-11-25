from services import Services
from enum import Enum


class Methods(Enum):
    start = 'start'
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
    register = 'register'


services = Services()

# routes/event


def follow(event):
    set_req_info(event)
    profile = services.app_service.line_bot_api.get_profile(
        services.app_service.req_user_id)
    services.reply_service.add_text(
        f'こんにちは。\n麻雀対戦結果自動管理アカウントである Mahjong Manager は{profile.display_name}さんの快適な麻雀生活をサポートします。')
    services.reply_service.reply(event)
    services.rich_menu_service.create_and_link('personal')


def join(event):
    set_req_info(event)
    services.reply_service.add_text(f'こんにちは、今日は麻雀日和ですね。')
    services.room_service.register()
    services.reply_service.reply(event)


def textMessage(event):
    set_req_info(event)
    routing_by_text(event)
    services.reply_service.reply(event)


def imageMessage(event):
    set_req_info(event)
    services.reply_service.add_text('画像への返信はまだサポートされていません。開発者に寄付をすれば対応を急ぎます。')
    services.reply_service.reply(event)


def postback(event):
    set_req_info(event)
    method = event.postback.data[1:]
    routing_by_method(method)
    services.reply_service.reply(event)


def set_req_info(event):
    services.app_service.req_user_id = event.source.user_id
    if event.source.type == 'room':
        services.app_service.req_room_id = event.source.room_id

# routes/text


def routing_by_text(event):
    text = event.message.text
    prefix = text[0]
    if (prefix == '_') & (text[1:] in [e.name for e in Methods]):
        routing_by_method(text[1:])
        return

    # routing by mode
    # inpuy mode
    if services.room_service.get_mode() == services.room_service.modes.input:
        services.points_service.add_by_text(text)
        return

    # delete mode
    if services.room_service.get_mode() == services.room_service.modes.delete:
        services.results_service.delete_by_text(text)
        return

    # off mode
    if services.room_service.get_mode() == services.room_service.modes.input:
        return

    # wait mode
    if prefix == '_':
        services.reply_service.add_text('使い方がわからない場合はメニューの中の「使い方」を押してください。')
        return
    services.reply_service.add_text('雑談してる暇があったら麻雀の勉強をしましょう')

# routes/text.method


def routing_by_method(method):
    # start
    if method == Methods.start.name:
        services.reply_service.add_start_menu()
    # register
    if method == Methods.register.name:
        services.room_service.register()
    # input
    if method == Methods.input.name:
        services.points_service.reset()
        services.room_service.chmod(services.room_service.modes.input)
    # calculate
    elif method == Methods.calc.name:
        services.calculate_service.calculate()
    # mode
    elif method == Methods.mode.name:
        services.room_service.reply_mode()
    # exit
    elif method == Methods.exit.name:
        services.room_service.chmod(services.room_service.modes.wait)
    # help
    elif method == Methods.help.name:
        services.reply_service.add_text('使い方は明日書きます。')
        services.reply_service.add_text(
            '\n'.join(['_' + e.name for e in Methods]))
    # setting
    elif method == Methods.setting.name:
        services.config_service.reply()
    # off
    elif method == Methods.off.name:
        services.room_service.chmod(services.room_service.modes.off)
    # on
    elif method == Methods.on.name:
        services.room_service.chmod(services.room_service.modes.wait)
    # reset
    elif method == Methods.reset.name:
        services.results_service.reset()
    # results
    elif method == Methods.results.name:
        services.results_service.reply_all()
    # delete
    elif method == Methods.delete.name:
        services.room_service.chmod(services.room_service.modes.delete)
    # finish
    elif method == Methods.finish.name:
        services.results_service.finish()
    # github
    elif method == Methods.github.name:
        services.reply_service.add_text(
            'https://github.com/bbladr/mahjong-manager-bot')
