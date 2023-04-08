from ApplicationModels.PageContents import PageContents
from repositories import (
    web_user_repository, session_scope
)


class DenyLinkLineUserUseCase():
    def execute(self, page_contents: PageContents) -> None:
        with session_scope() as db_session:
            web_user_repository.update_linked_line_user_id(
                session=db_session,
                id=page_contents.login_user._id,
                line_user_id='',
            )
            page_contents.message = '申請を取り消しました。'
