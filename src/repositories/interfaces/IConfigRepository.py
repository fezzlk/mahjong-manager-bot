from abc import ABCMeta, abstractmethod


class IConfigRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_one_by_target_id_and_key(self, session, target_id, key):
        pass

    @abstractmethod
    def find_all(self, session):
        pass

    @abstractmethod
    def find_by_target_id(self, session, target_id):
        pass

    @abstractmethod
    def find_by_ids(self, session, ids):
        pass

    @abstractmethod
    def create(self, session, new_config):
        pass

    @abstractmethod
    def delete_by_target_id_and_key(self, session, target_id, key):
        pass

    @abstractmethod
    def delete_by_ids(self, session, ids):
        pass
