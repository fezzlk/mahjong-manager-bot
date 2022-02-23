from DomainService import (
    group_service,
)

from ApplicationService import (
    request_info_service,
    reply_service,
)


class ReplyGroupZoomUrlUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        result_zoom_url = group_service.get_zoom_url(line_group_id)

        if result_zoom_url is None:
            reply_service.add_message('Zoom URL を取得できませんでした。')
            return

        reply_service.add_message(result_zoom_url)
