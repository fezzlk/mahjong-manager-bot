import threading
from typing import Dict, List

from linebot.v3.webhooks import Event


class RequestInfoService:
    """RequestInfoService

    メッセージ送信元の LINE ユーザー ID, トークルーム ID を管理。
    threading.local() でスレッドごとに独立した状態を持つ(マルチスレッド対応)。
    """

    def __init__(self):
        self._local = threading.local()

    def _state(self):
        local = self._local
        if not hasattr(local, "initialized"):
            local.req_line_user_id = None
            local.req_line_group_id = None
            local.mention_line_ids = []
            local.message = None
            local.command = None
            local.params = {}
            local.body = None
            local.is_mention_all = False
            local.initialized = True
        return local

    @property
    def req_line_user_id(self) -> str:
        return self._state().req_line_user_id

    @req_line_user_id.setter
    def req_line_user_id(self, value: str):
        self._state().req_line_user_id = value

    @property
    def req_line_group_id(self) -> str:
        return self._state().req_line_group_id

    @req_line_group_id.setter
    def req_line_group_id(self, value: str):
        self._state().req_line_group_id = value

    @property
    def mention_line_ids(self) -> List[str]:
        return self._state().mention_line_ids

    @mention_line_ids.setter
    def mention_line_ids(self, value: List[str]):
        self._state().mention_line_ids = value

    @property
    def message(self) -> str:
        return self._state().message

    @message.setter
    def message(self, value: str):
        self._state().message = value

    @property
    def command(self) -> str:
        return self._state().command

    @command.setter
    def command(self, value: str):
        self._state().command = value

    @property
    def params(self) -> Dict[str, str]:
        return self._state().params

    @params.setter
    def params(self, value: Dict[str, str]):
        self._state().params = value

    @property
    def body(self) -> str:
        return self._state().body

    @body.setter
    def body(self, value: str):
        self._state().body = value

    @property
    def is_mention_all(self) -> bool:
        return self._state().is_mention_all

    @is_mention_all.setter
    def is_mention_all(self, value: bool):
        self._state().is_mention_all = value

    def set_req_info(self, event: Event) -> None:
        self.req_line_user_id = event.source.user_id
        if event.source.type == "room":
            self.req_line_group_id = event.source.room_id
            import env_var  # noqa: PLC0415
            from application_service import reply_service  # noqa: PLC0415

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
                        from domain_service import user_group_service  # noqa: PLC0415

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
        from repositories import command_alias_repository  # noqa: PLC0415

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

        if self.message.startswith("_") and len(self.message) > 1:
            command_and_params = self.message.split()[0]
            self.body = self.message[len(command_and_params) + 1 :]
            self.command = command_and_params.split("?")[0][1:]
            param_list = command_and_params[len(self.command) + 2 :].split("&")
            for p in param_list:
                k_v = p.split("=")
                if len(k_v) >= 2:
                    self.params[k_v[0]] = p[len(k_v[0]) + 1 :]

    def delete_req_info(self) -> None:
        """リクエスト完了後に当スレッドの状態をリセット"""
        state = self._state()
        state.req_line_user_id = None
        state.req_line_group_id = None
        state.mention_line_ids = []
        state.message = None
        state.command = None
        state.params = {}
        state.body = None
        state.is_mention_all = False
