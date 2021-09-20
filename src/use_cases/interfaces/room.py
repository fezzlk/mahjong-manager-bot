# flake8: noqa: E999
from abc import ABC, abstractmethod


class IRoomUseCases(ABC):

    @abstractmethod
    def join(self):
        pass

    @abstractmethod
    def wait_mode(self):
        pass

    @abstractmethod
    def input_mode(self):
        pass

    @abstractmethod
    def reply_mode(self):
        pass

    @abstractmethod
    def reset_points(self):
        pass

    @abstractmethod
    def reply_sum_results(self, body: str):
        pass

    @abstractmethod
    def reply_zoom_url(self):
        pass

    @abstractmethod
    def set_zoom_url(self, zoom_id: str):
        pass

    @abstractmethod
    def get(self, ids: list):
        pass

    @abstractmethod
    def delete(self, ids: list):
        pass
