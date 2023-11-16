from linebot.models.events import Event
from typing import List, Dict

class RequestInfoService:
    """RequestInfoService
    メッセージ送信元の LINE ユーザー ID, トークルーム ID を管理
    """
    req_line_user_id: str
    req_line_group_id: str
    mention_line_ids: List[str]
    message: str
    method: str
    body: str
    params: Dict[str, str]

    def __init__(self):
        # 送信元の LINE ユーザー ID, トークルーム ID, グループ ID
        self.req_line_user_id = None
        self.req_line_group_id = None
        self.mention_line_ids = []
        self.message = None
        self.method = None
        self.params = {}
        self.body = None

    """
    メッセージ送信元情報のセット
    """

    def set_req_info(self, event: Event) -> None:

        self.req_line_user_id = event.source.user_id
        if event.source.type == 'room':
            self.req_line_group_id = event.source.room_id
        if event.source.type == 'group':
            self.req_line_group_id = event.source.group_id

        if event.type == 'message':
            if hasattr(event.message, 'text'):
                self.message = event.message.text
                self.parse_message()
                if hasattr(event.message, 'mention') and event.message.mention is not None:
                    mentionees = event.message.mention.mentionees
                    for mentionee in mentionees:
                        self.mention_line_ids.append(mentionee.user_id)

    def parse_message(self):
        if self.message is None or self.message == '':
            return
        if (self.message[0] == '_') & (len(self.message) > 1):
            method_and_params = self.message.split()[0]
            self.body = self.message[len(method_and_params) + 1:]
            self.method = method_and_params.split('?')[0][1:]
            param_list = method_and_params[len(self.method) + 2:].split('&')
            for p in param_list:
                k_v = p.split('=')
                if len(k_v) >= 2:
                    self.params[k_v[0]] = p[len(k_v[0]) + 1:]

    """
    メッセージ送信元情報の削除
    一つ前のメッセージ送信元の情報が残らないようにするために使う
    """

    def delete_req_info(self) -> None:
        self.req_line_user_id = None
        self.req_line_group_id = None
        self.mention_line_ids = []
        self.message = None
        self.method = None
        self.params = []
        self.body = None
