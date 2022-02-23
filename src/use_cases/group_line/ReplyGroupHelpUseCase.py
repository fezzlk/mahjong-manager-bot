from typing import List
from ApplicationService import (
    reply_service,
)


class ReplyGroupHelpUseCase:

    def execute(self, RCommands: List[str]) -> None:
        reply_service.add_message('使い方は明日書きます。')
        reply_service.add_message(
            '\n'.join(['_' + e.name for e in RCommands]))
