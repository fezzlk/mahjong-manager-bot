from abc import ABC, abstractmethod


class IConfigUseCases(ABC):

    @abstractmethod
    def reply_menu(self):
        pass

    @abstractmethod
    def update(self):
        pass
