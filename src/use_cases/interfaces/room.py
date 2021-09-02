from abc import ABC, abstractmethod


class IRoomUseCases(ABC):

    @abstractmethod
    def join(self):
        pass
