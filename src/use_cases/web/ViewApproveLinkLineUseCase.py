from ApplicationModels.PageContents import PageContents
from repositories import (
    web_user_repository, user_repository, session_scope
)
from DomainModel.entities.WebUser import WebUser
from DomainModel.entities.User import User


class ViewApproveLinkLineUseCase():
    def execute(
            self,
            page_contents: PageContents
    ) -> PageContents:
        page_contents.page_title = 'LINEアカウント連携'

        with session_scope() as session:
            login_user: WebUser = web_user_repository.find_by_id(
                session=session,
                _id=page_contents.login_user._id
            )

            page_contents.line_user_name = ''
            if login_user is not None:
                line_user: User = user_repository.find_one_by_line_user_id(
                    session=session,
                    line_user_id=login_user.linked_line_user_id
                )

                if line_user is not None:
                    page_contents.line_user_name = line_user.line_user_name

            return page_contents
