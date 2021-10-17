from abc import ABC, abstractmethod


class IConfigUseCases(ABC):

    @abstractmethod
    def reply_menu(self):
        pass

    @abstractmethod
    def update(self, key: str, value: str):
        pass

    @abstractmethod
    def get(self, ids: list):
        pass

    @abstractmethod
    def delete(self, ids: list):
        pass
