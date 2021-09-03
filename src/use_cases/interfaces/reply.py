from abc import ABC, abstractmethod


class IReplyUseCases(ABC):

    @abstractmethod
    def add_start_menu(self):
        pass

    @abstractmethod
    def add_others_menu(self):
        pass
