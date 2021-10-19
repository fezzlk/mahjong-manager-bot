from abc import ABCMeta, abstractmethod


class IRichMenuService(metaclass=ABCMeta):

    @abstractmethod
    def create_and_link(self, line_user_id: str) -> None:
        pass
