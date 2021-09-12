# flake8: noqa: E999
from abc import ABC, abstractmethod


class IPointsUseCases(ABC):

    @abstractmethod
    def add_by_text(self, text: str):
        pass

    @abstractmethod
    def reply(self, result: object):
        pass
