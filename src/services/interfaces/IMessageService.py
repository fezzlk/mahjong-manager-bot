from abc import ABCMeta, abstractmethod


class IMessageService(metaclass=ABCMeta):

    @abstractmethod
    def get_random_hai(
        self,
        line_user_id: str,
    ) -> str:
        pass

    @abstractmethod
    def get_wait_massage(self) -> str:
        pass

    @abstractmethod
    def get_finish_hanchan_message(self) -> str:
        pass
