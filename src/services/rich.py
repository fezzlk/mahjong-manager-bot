"""rich menu"""

from linebot.models import (
    RichMenu,
    RichMenuSize,
    RichMenuArea,
    RichMenuBounds,
    PostbackTemplateAction,
)


class RichMenuService:
    """rich menu service"""

    def __init__(self, services):
        self.services = services

    def create_and_link(self):
        rich_menu_id = self.create_personal_menu()

        self.services.app_service.line_bot_api.link_rich_menu_to_user(
            self.services.app_service.req_user_id, rich_menu_id
        )

    def create_personal_menu(self):
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=2500, height=1100),
            selected=False,
            name="personal menu",
            chat_bar_text="メニュー",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=833, height=550),
                    action=PostbackTemplateAction(
                        label='payment',
                        display_text='支払いするにゃっ',
                        data='_payment'
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=833, y=0, width=834, height=550),
                    action=PostbackTemplateAction(
                        label='analysis',
                        display_text='分析するにゃっ',
                        data='_analysis'
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1667, y=0, width=833, height=550),
                    action=PostbackTemplateAction(
                        label='fortune',
                        display_text='占って欲しいにゃっ',
                        data='_fortune'
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=550, width=833, height=550),
                    action=PostbackTemplateAction(
                        label='history',
                        display_text='対戦履歴を見たいにゃっ',
                        data='_history'
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=833, y=550, width=834, height=550),
                    action=PostbackTemplateAction(
                        label='help',
                        display_text='使い方がわからないにゃっ',
                        data='_help'
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=1667, y=550, width=833, height=550),
                    action=PostbackTemplateAction(
                        label='config',
                        display_text='設定変更するにゃっ',
                        data='_setting'
                    )
                )
            ]
        )
        rich_menu_id = self.services.app_service.line_bot_api.create_rich_menu(
            rich_menu=rich_menu_to_create
        )
        file_path = './static/images/rich/personal.png'
        content_type = 'Image/png'
        with open(file_path, 'rb') as f:
            self.services.app_service.line_bot_api.set_rich_menu_image(
                rich_menu_id, content_type, f)
        return rich_menu_id
