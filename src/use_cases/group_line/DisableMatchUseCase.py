from DomainService import (
    match_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
)
from repositories import hanchan_repository


class DisableMatchUseCase:

    def execute(self) -> None:
        match = match_service.update_status_active_match(
            request_info_service.req_line_group_id,
            0,
        )
        hanchan_repository.update(
            {
                'match_id': match._id,
                'status': 1
            },
            {'status': 0},
        )

        reply_service.add_message('前回の対戦結果を削除しました。')