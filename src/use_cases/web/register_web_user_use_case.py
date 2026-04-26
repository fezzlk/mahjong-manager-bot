from werkzeug.exceptions import BadRequest

from application_models.page_contents import PageContents
from application_models.register_web_user_form import RegisterWebUserForm
from domain_model.entities.web_user import WebUser
from repositories import web_user_repository


class RegisterWebUserUseCase:
    def execute(self, page_contents: PageContents) -> str:
        request = page_contents.request
        form = RegisterWebUserForm(request.form)

        if not form.validate():
            raise BadRequest(
                ", ".join([f"{k}: {v}" for k, v in form.errors.items()]))

        new_web_user = WebUser(
            user_code=form.email.data,
            email=form.email.data,
            name=form.name.data,
        )

        web_user_repository.create(
            new_record=new_web_user,
        )

        return None
