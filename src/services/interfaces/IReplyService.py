from abc import ABCMeta, abstractmethod


class IReplyService(metaclass=ABCMeta):
    @abstractmethod
    def add_message(
        self,
        text: str,
    ) -> None:
        pass
