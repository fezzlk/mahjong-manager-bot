from abc import ABCMeta, abstractmethod


class IUserService(metaclass=ABCMeta):

    @abstractmethod
    def get_user_id_by_name(
        self,
        name: str,
    ) -> str:
        pass

    @abstractmethod
    def get_name_by_line_user_id(
        self,
        line_user_id: str,
    ) -> str:
        pass
