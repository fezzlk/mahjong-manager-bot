from application_models.page_contents import PageContents
from repositories import web_user_repository


class DenyLinkLineUserUseCase:
    def execute(self, page_contents: PageContents) -> None:
        web_user_repository.update_linked_line_user_id(
            _id=page_contents.login_user._id,
            line_user_id="",
        )
        page_contents.message = "申請を取り消しました。"
