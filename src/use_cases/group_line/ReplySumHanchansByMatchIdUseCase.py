# from DomainService import (
#     user_service,
#     match_service,
# )
# from ApplicationService import (
#     reply_service,
#     request_info_service,
# )
# from repositories import match_repository, hanchan_repository
# from typing import Optional


# class ReplySumHanchansByMatchIdUseCase:

#     def execute(self, match_id: Optional[int] = None) -> None:
#         if match_id is None:
#             match = match_service.get_current(request_info_service.req_line_group_id)
#         else:
#             matches = match_repository.find(
#                 {'_id': match_id},
#             )
#             if len(matches) == 0:
#                 reply_service.add_message(f'対戦ID={match_id}の対戦結果が見つかりませんでした。')
#             match = matches[0]

#         date = match.created_at.strftime('%Y-%m-%d') + '\n',
#         hanchans = hanchan_repository.find(
#             {'match_id': matches[0]._id})

#         hanchans_message_list = []
#         sum_hanchans = {}

#         for i in range(len(hanchans)):
#             converted_scores = hanchans[i].converted_scores
#             hanchans_message_list.append(
#                 f'第{i+1}回\n' + '\n'.join([
#                     f'{user_service.get_name_by_line_user_id(r[0])}: {"+" if r[1] > 0 else ""}{r[1]}'
#                     for r in sorted(
#                         converted_scores.items(),
#                         key=lambda x:x[1],
#                         reverse=True
#                     )
#                 ])
#             )

#             for line_user_id, converted_score in converted_scores.items():
#                 if line_user_id not in sum_hanchans.keys():
#                     sum_hanchans[line_user_id] = 0

#                 sum_hanchans[line_user_id] += converted_score

#         reply_service.add_message('\n\n'.join(hanchans_message_list))
#         reply_service.add_message(
#             '総計\n' + date + '\n'.join([
#                 f'{user_service.get_name_by_line_user_id(r[0])}: {"+" if r[1] > 0 else ""}{r[1]}'
#                 for r in sorted(
#                     sum_hanchans.items(),
#                     key=lambda x:x[1],
#                     reverse=True
#                 )
#             ])
#         )
