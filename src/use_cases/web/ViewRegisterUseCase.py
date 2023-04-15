from flask import (
    request,
)
from typing import Tuple
from ApplicationModels.RegisterWebUserForm import RegisterWebUserForm
from ApplicationModels.PageContents import PageContents, RegisterFormData


class ViewRegisterUseCase():
    def execute(
        self,
        page_contents: PageContents[RegisterFormData]
    ) -> Tuple[PageContents[RegisterFormData], RegisterWebUserForm]:
        page_contents.page_title = 'ユーザー登録'
        form = RegisterWebUserForm(request.form)

        form.name.data = page_contents.data.login_name
        form.email.data = page_contents.data.login_email

        return page_contents, form
