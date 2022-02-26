from DomainService import (
    group_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)


class JoinGroupUseCase:

    def execute(self) -> None:
        reply_service.add_message(
            'こんにちは、今日は麻雀日和ですね。'
        )
        line_group_id = request_info_service.req_line_group_id
        if line_group_id is None:
            print('This request is not from group chat')
            return
        group_service.find_or_create(line_group_id)
