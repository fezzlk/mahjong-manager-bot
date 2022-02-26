from abc import ABCMeta, abstractmethod
from typing import Dict


class IConfigService(metaclass=ABCMeta):

    @abstractmethod
    def get_current_settings_by_target(
        self,
        target_id: str,
    ) -> Dict[str, str]:
        pass

    @abstractmethod
    def get_value_by_key(
        self,
        target_id: str,
        key: str,
    ) -> str:
        pass

    @abstractmethod
    def update_setting(
        self,
        target_id: str,
        key: str,
        value: str,
    ) -> None:
        pass