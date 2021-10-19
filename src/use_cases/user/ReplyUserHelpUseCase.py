from typing import List
from services import (
    reply_service,
)


class ReplyUserHelpUseCase:

    def execute(self, UCommands: List[str]) -> None:
        reply_service.add_message('使い方は明日書きます。')
        reply_service.add_message(
            '\n'.join(['_' + e.name for e in UCommands])
        )