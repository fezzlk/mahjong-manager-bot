# from DomainService import (
#     match_service,
#     group_service,
# )
# from ApplicationService import (
#     request_info_service,
#     reply_service,
# )
# from repositories import hanchan_repository


# class DisableMatchUseCase:

#     def execute(self) -> None:
#         line_group_id = request_info_service.req_line_group_id
#         group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
#         if group is None:
#             reply_service.add_message(
#                 'グループが登録されていません。招待し直してください。'
#             )
#             return
#         active = match_service.update_status_active_match(
#             request_info_service.req_line_group_id,
#             0,
#         )

#         reply_service.add_message('現在登録中の試合結果を削除しました。')