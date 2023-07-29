# from DomainModel.entities.Match import Match
# from repositories import session_scope, match_repository


# class GetMatchForWebUseCase:

#     def execute(self, id) -> Match:
#         with session_scope() as session:
#             records = match_repository.find(session, [_id])
#             if len(records) > 0:
#                 return records[0]
#             else:
#                 None
