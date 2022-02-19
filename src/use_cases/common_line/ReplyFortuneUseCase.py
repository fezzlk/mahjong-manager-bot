from Services import (
    request_info_service,
    reply_service,
    user_service,
    message_service,
)


class ReplyFortuneUseCase:

    def execute(self) -> None:
        line_user_id = request_info_service.req_line_user_id
        user_name = user_service.get_name_by_line_user_id(line_user_id)
        lucky_hai = message_service.get_random_hai(line_user_id)
        reply_service.add_message(
            f'{user_name}さんの今日のラッキー牌は「{lucky_hai}」です。'
        )
