# flake8: noqa: E999
from abc import ABC, abstractmethod


class IUserUseCases(ABC):

    @abstractmethod
    def follow(self):
        pass

    @abstractmethod
    def unfollow(self):
        pass

    @abstractmethod
    def set_zoom_id(self, zoom_id: str):
        pass

    @abstractmethod
    def reply_mode(self):
        pass

    @abstractmethod
    def chmod(self, user_id: str, mode: str):
        pass

    @abstractmethod
    def reply_zoom_id(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def create(self, name: str, user_id: str):
        pass

    @abstractmethod
    def delete(self, ids: list):
        pass
