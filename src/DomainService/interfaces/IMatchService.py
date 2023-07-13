from abc import ABCMeta, abstractmethod
from DomainModel.entities.Match import Match


class IMatchService(metaclass=ABCMeta):

    # @abstractmethod
    # def add_hanchan_id(
    #     self,
    #     line_group_id: str,
    #     hanchan_id: int,
    # ) -> Match:
    #     pass

    @abstractmethod
    def get_current(self, line_group_id: str) -> Match:
        pass

    # @abstractmethod
    # def update_current_status(
    #     self,
    #     line_group_id: str,
    #     status: int,
    # ) -> Match:
    #     pass

    # @abstractmethod
    # def archive(self, line_group_id: str) -> Match:
    #     pass

    # @abstractmethod
    # def disable(self, line_group_id: str) -> Match:
    #     pass

    @abstractmethod
    def find_or_create_current(self, line_group_id: str) -> Match:
        pass

    # @abstractmethod
    # def remove_hanchan_id(
    #     self,
    #     match_id: int,
    #     hanchan_id: int,
    # ) -> Match:
    #     pass
