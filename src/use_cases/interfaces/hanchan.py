from abc import ABC, abstractmethod


class IHanchanUseCases(ABC):

    @abstractmethod
    def add(self, points=dict):
        pass

    @abstractmethod
    def get(self, ids: list):
        pass

    @abstractmethod
    def delete(self, ids: list):
        pass

    @abstractmethod
    def migrate(self):
        pass
