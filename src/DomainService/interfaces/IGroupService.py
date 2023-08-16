from abc import ABCMeta, abstractmethod
from DomainModel.entities.Group import Group, GroupMode


class IGroupService(metaclass=ABCMeta):

    @abstractmethod
    def chmod(
        self,
        line_group_id: str,
        mode: GroupMode,
    ) -> None:
        pass

    @abstractmethod
    def find_or_create(self, line_group_id: str) -> Group:
        pass

    @abstractmethod
    def get_mode(self, line_group_id: str) -> GroupMode:
        pass

    @abstractmethod
    def update(self, target: Group) -> None:
        pass

    @abstractmethod
    def delete_by_line_group_id(self, line_group_id: str) -> None:
        pass
