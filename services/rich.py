from linebot.models import (
    RichMenu,
    RichMenuSize,
    RichMenuArea,
    RichMenuBounds,
    PostbackTemplateAction,
)
    
class RichMenuService:

    def __init__(self, app_service):
        self.menu = None
        self.app_service = app_service
        self.line_bot_api = self.app_service.line_bot_api

    def create_and_link(self, kind):
        if kind == 'personal':
            rich_menu_id = self.create_personal_menu()
        else:
            rich_menu_id = self.create_personal_menu()

        self.line_bot_api.link_rich_menu_to_user(self.app_service.req_user_id, rich_menu_id)


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
                        label='OFF',
                        data='hoge'
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=833, y=0, width=834, height=550),
                    action=PostbackTemplateAction(
                        label='OFF',
                        data='fuga'
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1667, y=0, width=833, height=550),
                    action=PostbackTemplateAction(
                        label='OFF',
                        data='foo'
                    )
                ),
                            RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=550, width=833, height=550),
                    action=PostbackTemplateAction(
                        label='OFF',
                        data='1'
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=833, y=550, width=834, height=550),
                    action=PostbackTemplateAction(
                        label='OFF',
                        data='2'
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1667, y=550, width=833, height=550),
                    action=PostbackTemplateAction(
                        label='OFF',
                        data='3'
                    )
                )
            ]
        ) 
        rich_menu_id = self.line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        file_path = './images/rich/personal.png'
        content_type = 'Image/png'
        with open(file_path, 'rb') as f:
            self.line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)
        return rich_menu_id