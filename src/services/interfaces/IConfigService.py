from abc import ABCMeta, abstractmethod
from typing import List
from domains.Config import Config


class IConfigService(metaclass=ABCMeta):

    @abstractmethod
    def get_by_target(
        self,
        target_id: str,
    ) -> List[Config]:
        pass
