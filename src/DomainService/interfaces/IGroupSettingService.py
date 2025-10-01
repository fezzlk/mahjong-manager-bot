from abc import ABCMeta, abstractmethod

from DomainModel.entities.GroupSetting import GroupSetting


class IGroupSettingService(metaclass=ABCMeta):

    @abstractmethod
    def find_or_create(self, line_group_id: str) -> GroupSetting:
        pass
