from flask import session

from application_models.page_contents import PageContents, ViewUserInfoData
from messaging_api_setting import line_bot_api
from repositories import web_user_repository


class ViewUserInfoUseCase:
    def execute(
        self,
        page_contents: PageContents[ViewUserInfoData],
    ) -> PageContents[ViewUserInfoData]:
        page_contents.page_title = "プロフィール"

        login_user_id: str = session.get("login_user_id", None)
        login_user = web_user_repository.find_by_id(
            _id=login_user_id,
        )

        if login_user is not None:
            page_contents.data.user_name = login_user.name
            page_contents.data.user_email = login_user.email
            line_name = "未連携"
            if login_user.is_approved_line_user:
                profile = line_bot_api.get_profile(
                    login_user.linked_line_user_id,
                )
                line_name = profile.display_name
            page_contents.data.line_name = line_name

        return page_contents
