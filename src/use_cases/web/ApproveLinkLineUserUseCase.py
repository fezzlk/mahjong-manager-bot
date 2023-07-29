# from ApplicationModels.PageContents import PageContents
# from repositories import (
#     web_user_repository, session_scope
# )


# class ApproveLinkLineUserUseCase():
#     def execute(self, page_contents: PageContents) -> None:
#         with session_scope() as db_session:
#             web_user_repository.approve_line(
#                 session=db_session,
#                 _id=page_contents.login_user._id
#             )
#             page_contents.message = 'LINEアカウント連携を承認しました。'
