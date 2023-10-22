from typing import List
from ApplicationService import (
    reply_service,
)


class ReplyUserHelpUseCase:

    def execute(self, UCommands: List[str]) -> None:
        messages = []
        messages.append('個人チャットでは以下の機能を利用できます。')
        messages.append('【対戦履歴の参照】\nメニューの「対戦履歴」ボタンまたはメッセージ「_history」の送信で対戦履歴を表示します。対戦履歴がない場合はグループチャットにて対戦結果を入力する必要があります。')
        reply_service.add_message('\n\n'.join(messages))

