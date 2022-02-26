from abc import ABCMeta, abstractmethod
from linebot.models.events import Event


class IRequestInfoService(metaclass=ABCMeta):

    @abstractmethod
    def set_req_info(self, event: Event) -> None:
        pass

    @abstractmethod
    def delete_req_info(self) -> None:
        pass
