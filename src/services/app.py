class AppService:
    """AppService
    メッセージ送信元の LINE ユーザー ID, トークルーム ID を管理
    """

    def __init__(self):
        # 送信元の LINE ユーザー ID, トークルーム ID
        self.req_user_id = None
        self.req_room_id = None

    """
    メッセージ送信元情報のセット
    """
    def set_req_info(self, event):
        self.req_user_id = event.source.user_id
        if event.source.type == 'room':
            self.req_room_id = event.source.room_id

    """
    メッセージ送信元情報の削除
    一つ前のメッセージ送信元の情報が残らないようにするために使う
    """
    def delete_req_info(self):
        self.req_user_id = None
        self.req_room_id = None
