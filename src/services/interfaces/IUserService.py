from abc import ABCMeta, abstractmethod
from linebot.models.responses import Profile
from domains.User import User, UserMode


class IUserService(metaclass=ABCMeta):

    @abstractmethod
    def get_user_id_by_name(
        self,
        name: str,
    ) -> str:
        pass

    @abstractmethod
    def get_name_by_line_user_id(
        self,
        line_user_id: str,
    ) -> str:
        pass

    @abstractmethod
    def find_or_create_by_profile(
        self,
        profile: Profile,
    ) -> User:
        pass

    @abstractmethod
    def create(
        self,
        name: str,
        user_id: str,
    ) -> User:
        pass

    @abstractmethod
    def delete_one_by_line_user_id(self, user_id: str) -> None:
        pass

    @abstractmethod
    def get_zoom_url(self, line_user_id: str) -> str:
        pass

    @abstractmethod
    def set_zoom_url(
        self,
        line_user_id: str,
        zoom_url: str,
    ) -> User:
        pass

    @abstractmethod
    def get_mode(self, user_id: str) -> UserMode:
        pass
