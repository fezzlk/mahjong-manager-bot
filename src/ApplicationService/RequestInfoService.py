from typing import Dict, List

from linebot.models.events import Event


class RequestInfoService:
    """RequestInfoService

    メッセージ送信元の LINE ユーザー ID, トークルーム ID を管理
    """

    req_line_user_id: str
    req_line_group_id: str
    mention_line_ids: List[str]
    message: str
    command: str
    body: str
    params: Dict[str, str]
    is_mention_all: bool

    def __init__(self):
        # 送信元の LINE ユーザー ID, トークルーム ID, グループ ID
        self.req_line_user_id = None
        self.req_line_group_id = None
        self.mention_line_ids = []
        self.message = None
        self.command = None
        self.params = {}
        self.body = None
        self.is_mention_all = False

    """
    メッセージ送信元情報のセット
    """

    def set_req_info(self, event: Event) -> None:
        self.req_line_user_id = event.source.user_id
        if event.source.type == "room":
            self.req_line_group_id = event.source.room_id
            import env_var
            from ApplicationService import reply_service

            messages = [
                "source id: room からのイベントを受け取りました。",
                self.req_line_user_id,
                self.req_line_group_id,
            ]
            reply_service.push_a_message(
                to=env_var.SERVER_ADMIN_LINE_USER_ID,
                message="\n".join(messages),
            )
        if event.source.type == "group":
            self.req_line_group_id = event.source.group_id

        if event.type == "postback" and hasattr(event.postback, "data"):
            self.message = event.postback.data
            self.parse_message()
        if event.type == "message" and hasattr(event.message, "text"):
            self.message = event.message.text
            self.parse_message()
            if hasattr(event.message, "mention") and event.message.mention is not None:
                mentionees = event.message.mention.mentionees
                for mentionee in mentionees:
                    if hasattr(mentionee, "user_id") and mentionee.user_id is not None:
                        self.mention_line_ids.append(mentionee.user_id)
                    elif "@All" in self.message:
                        from DomainService import user_group_service

                        user_groups = user_group_service.find_all_by_line_group_id(
                            self.req_line_group_id,
                        )
                        line_user_ids_in_group = [ug.line_user_id for ug in user_groups]
                        self.mention_line_ids += line_user_ids_in_group
                        self.is_mention_all = True
                    if len(self.mention_line_ids) != 0:
                        self.mention_line_ids = list(set(self.mention_line_ids))

    def parse_message(self):
        if self.message is None or self.message == "":
            return

        # コマンドエイリアスの確認
        from repositories import command_alias_repository

        query = {
            "line_user_id": self.req_line_user_id,
            "alias": self.message,
        }
        if self.req_line_group_id is not None:
            query["line_group_id"] = self.req_line_group_id
        command_alias = command_alias_repository.find(query)
        if len(command_alias) != 0:
            self.message = command_alias[0].command
            self.mention_line_ids = command_alias[0].mentionees

        if (self.message[0] == "_") & (len(self.message) > 1):
            command_and_params = self.message.split()[0]
            self.body = self.message[len(command_and_params) + 1 :]
            self.command = command_and_params.split("?")[0][1:]
            param_list = command_and_params[len(self.command) + 2 :].split("&")
            for p in param_list:
                k_v = p.split("=")
                if len(k_v) >= 2:
                    self.params[k_v[0]] = p[len(k_v[0]) + 1 :]

    """
    メッセージ送信元情報の削除
    一つ前のメッセージ送信元の情報が残らないようにするために使う
    """

    def delete_req_info(self) -> None:
        self.req_line_user_id = None
        self.req_line_group_id = None
        self.mention_line_ids = []
        self.message = None
        self.command = None
        self.params = {}
        self.body = None
        self.is_mention_all = False
