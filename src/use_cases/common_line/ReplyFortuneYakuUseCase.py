from DomainService import (
    user_service,
)

from ApplicationService import (
    request_info_service,
    reply_service,
    message_service,
)


class ReplyFortuneYakuUseCase:

    def execute(self) -> None:
        # line_user_id = request_info_service.req_line_user_id
        # user_name = user_service.get_name_by_line_user_id(line_user_id)
        # if user_name is None:
        #     reply_service.add_message(
        #         'ユーザーが登録されていません。友達追加してください。'
        #     )    
        #     return
        # lucky_yaku = message_service.get_random_hai(line_user_id)
        # reply_service.add_message(
        #     f'{user_name}さんの今日のラッキー牌は「{lucky_yaku}」です。')
        
        #適当なコメントを返す
        reply_service.add_message('text')

