from linebot.models.events import Event


class RequestInfoService:
    """RequestInfoService
    メッセージ送信元の LINE ユーザー ID, トークルーム ID を管理
    """

    def __init__(self):
        # 送信元の LINE ユーザー ID, トークルーム ID, グループ ID
        self.req_line_user_id = None
        self.req_line_group_id = None

    """
    メッセージ送信元情報のセット
    """
    def set_req_info(self, event: Event) -> None:
        self.req_line_user_id = event.source.user_id
        if event.source.type == 'room':
            self.req_line_group_id = event.source.room_id
        if event.source.type == 'group':
            self.req_line_group_id = event.source.group_id

    """
    メッセージ送信元情報の削除
    一つ前のメッセージ送信元の情報が残らないようにするために使う
    """
    def delete_req_info(self) -> None:
        self.req_line_user_id = None
        self.req_line_group_id = None