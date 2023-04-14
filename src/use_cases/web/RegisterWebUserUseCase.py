from werkzeug.exceptions import BadRequest

from DomainModel.entities.WebUser import WebUser
from ApplicationModels.PageContents import PageContents
from ApplicationModels.RegisterWebUserForm import RegisterWebUserForm
from repositories import web_user_repository, session_scope


class RegisterWebUserUseCase():
    def execute(self, page_contents: PageContents) -> str:
        request = page_contents.request
        form = RegisterWebUserForm(request.form)

        if not form.validate():
            raise BadRequest(
                ', '.join([f'{k}: {v}' for k, v in form.errors.items()]))

        new_web_user = WebUser(
            user_code=form.email.data,
            email=form.email.data,
            name=form.name.data,
        )

        with session_scope() as session:
            web_user_repository.create(
                session=session,
                new_web_user=new_web_user
            )

        return
