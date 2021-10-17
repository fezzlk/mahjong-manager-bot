from abc import ABCMeta, abstractmethod


class IConfigRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_one_by_room_id(self, session, room_id):
        pass

    @abstractmethod
    def find_by_ids(self, session, ids):
        pass

    @abstractmethod
    def find_all(self, session):
        pass

    @abstractmethod
    def create(self, session, new_room):
        pass

    @abstractmethod
    def delete_by_ids(self, session, ids):
        pass

    @abstractmethod
    def update_one_mode_by_line_room_id(self, session, line_room_id, mode):
        pass

    @abstractmethod
    def update_one_zoom_url_by_line_room_id(
        self,
        session,
        line_room_id,
        zoom_url,
    ):
        pass
