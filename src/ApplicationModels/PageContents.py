from dataclasses import dataclass
from typing import Generic, TypeVar
from flask import Request
from flask.sessions import SessionMixin
from DomainModel.entities.WebUser import WebUser
from repositories import web_user_repository


@dataclass()
class RegisterFormData:
    login_name: str
    login_email: str

    def __init__(
        self,
        session: SessionMixin,
    ):
        self.login_name = session['login_name']
        self.login_email = session['login_email']


@dataclass()
class ViewUserInfoData():
    user_name: str
    user_email: str
    line_name: str

    def __init__(
        self,
        session: SessionMixin,
    ):
        pass


T = TypeVar('T', RegisterFormData, ViewUserInfoData, None)


@dataclass()
class PageContents(Generic[T]):
    session: dict
    request: Request
    page_title: str
    login_user: WebUser
    line_user_name: str
    next_page_url: str
    data: T
    message: str

    def __init__(
        self,
        session: SessionMixin,
        request: Request,
        DataClass: T = None,
        page_title: str = '',
    ):
        self.session = dict(session)
        self.login_user = None
        login_user_id: str = session.get('login_user_id', None)
        login_user = web_user_repository.find(
            {'_id': login_user_id}
        )

        if login_user is not None:
            self.login_user = login_user

        self.next_page_url = session.get('next_page_url', '')
        self.line_user_name = ''
        self.page_title = page_title
        self.request = request
        self.message = session.get('message', '')
        if DataClass is not None:
            self.data = DataClass(session)
