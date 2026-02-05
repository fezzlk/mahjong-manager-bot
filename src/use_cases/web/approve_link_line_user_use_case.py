from application_models.page_contents import PageContents
from repositories import web_user_repository


class ApproveLinkLineUserUseCase:
    def execute(self, page_contents: PageContents) -> None:
        web_user_repository.approve_line(
            _id=page_contents.login_user._id,
        )
        page_contents.message = "LINEアカウント連携を承認しました。"
