from Services import (
    reply_service,
)


class ReplyGitHubUrlUseCase:

    def execute(self) -> None:
        reply_service.add_message(
            'https://github.com/bbladr/mahjong-manager-bot'
        )
