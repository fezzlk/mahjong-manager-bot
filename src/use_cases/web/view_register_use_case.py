from typing import Tuple

from flask import (
    request,
)

from application_models.page_contents import PageContents, RegisterFormData
from application_models.register_web_user_form import RegisterWebUserForm


class ViewRegisterUseCase:
    def execute(
        self,
        page_contents: PageContents[RegisterFormData],
    ) -> Tuple[PageContents[RegisterFormData], RegisterWebUserForm]:
        page_contents.page_title = "ユーザー登録"
        form = RegisterWebUserForm(request.form)

        form.name.data = page_contents.data.login_name
        form.email.data = page_contents.data.login_email

        return page_contents, form
