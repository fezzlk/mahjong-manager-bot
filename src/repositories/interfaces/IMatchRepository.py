from abc import ABCMeta, abstractmethod


class IConfigRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_by_ids(self, session, ids):
        pass

    @abstractmethod
    def find_one_by_line_room_id_and_status(
        self,
        session,
        line_room_id,
        status,
    ):
        pass

    @abstractmethod
    def find_many_by_room_id_and_status(self, session, line_room_id, status):
        pass

    @abstractmethod
    def create(self, session, new_match):
        pass

    @abstractmethod
    def find_all(self, session):
        pass

    @abstractmethod
    def add_hanchan_id_by_line_room_id(
        self,
        session,
        line_room_id,
        hanchan_id,
    ):
        pass

    @abstractmethod
    def update_one_status_by_line_room_id(
        self,
        session,
        line_room_id,
        status,
    ):
        pass

    @abstractmethod
    def update_one_hanchan_ids_by_line_room_id(
        self,
        session,
        line_room_id,
        hanchan_ids,
    ):
        pass

    @abstractmethod
    def remove_hanchan_id_by_id(
        self,
        session,
        match_id,
        hanchan_id,
    ):
        pass
