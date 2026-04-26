"""rich menu"""

from linebot.v3.messaging import (
    MessagingApiBlob,
    PostbackAction,
    RichMenuArea,
    RichMenuBounds,
    RichMenuRequest,
    RichMenuSize,
)

from messaging_api_setting import _api_client, line_bot_api


class RichMenuService:

    def create_and_link(self, line_user_id: str) -> None:
        rich_menu_id = self._create_personal_menu()

        line_bot_api.link_rich_menu_id_to_user(
            user_id=line_user_id,
            rich_menu_id=rich_menu_id,
        )

    def _create_personal_menu(self) -> str:
        rich_menu_to_create = RichMenuRequest(
            size=RichMenuSize(width=2500, height=1100),
            selected=False,
            name="personal menu",
            chat_bar_text="メニュー",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=833, height=550),
                    action=PostbackAction(
                        label="payment",
                        display_text="支払いするにゃっ",
                        data="_payment",
                    ),
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=833, y=0, width=834, height=550),
                    action=PostbackAction(
                        label="analysis",
                        display_text="分析するにゃっ",
                        data="_analysis",
                    ),
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1667, y=0, width=833, height=550),
                    action=PostbackAction(
                        label="fortune",
                        display_text="占って欲しいにゃっ",
                        data="_fortune",
                    ),
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=550, width=833, height=550),
                    action=PostbackAction(
                        label="history",
                        display_text="対戦履歴を見たいにゃっ",
                        data="_history",
                    ),
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=833, y=550, width=834, height=550),
                    action=PostbackAction(
                        label="help",
                        display_text="使い方がわからないにゃっ",
                        data="_help",
                    ),
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=1667, y=550, width=833, height=550),
                    action=PostbackAction(
                        label="config",
                        display_text="設定変更するにゃっ",
                        data="_setting",
                    ),
                ),
            ],
        )

        response = line_bot_api.create_rich_menu(rich_menu_request=rich_menu_to_create)
        rich_menu_id = response.rich_menu_id

        file_path = "src/static/images/rich/personal.png"
        blob_api = MessagingApiBlob(_api_client)
        with open(file_path, "rb") as f:
            blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=f.read(),
                _headers={"Content-Type": "image/png"},
            )

        return rich_menu_id
