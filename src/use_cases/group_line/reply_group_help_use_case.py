from typing import List

from application_service import (
    reply_service,
)


class ReplyGroupHelpUseCase:
    def execute(self, commands: List[str]) -> None:
        reply_service.add_message(
            "利用可能なコマンド一覧です。「_コマンド名」の形式で入力してください。"
        )
        reply_service.add_message("\n".join(f"_{name}" for name in commands))
