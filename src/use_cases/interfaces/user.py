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
