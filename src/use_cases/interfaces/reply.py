from abc import ABC, abstractmethod


class IReplyUseCases(ABC):

    @abstractmethod
    def add_start_menu(self):
        pass

    @abstractmethod
    def add_others_menu(self):
        pass

    @abstractmethod
    def reply_fortune(self):
        pass

    @abstractmethod
    def reply_user_help(self, UCommands: list):
        pass

    @abstractmethod
    def reply_room_help(self, RCommands: list):
        pass

    @abstractmethod
    def reply_github_url(self):
        pass
