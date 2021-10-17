from abc import ABCMeta, abstractmethod


class IConfigRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_one_by_id_and_line_room_id(
        self,
        session,
        target_id,
        line_room_id,
    ):
        pass

    @abstractmethod
    def find_one_by_line_room_id_and_status(
        self,
        session,
        line_room_id,
        status
    ):
        pass

    @abstractmethod
    def find_by_ids(self, session, ids):
        pass

    @abstractmethod
    def find_all(self, session):
        pass

    @abstractmethod
    def create(self, session, new_hanchan):
        pass

    @abstractmethod
    def delete_by_ids(self, session, ids):
        pass

    @abstractmethod
    def update_raw_score_of_user_by_room_id(
        self,
        session,
        line_room_id,
        line_user_id,
        raw_score=None,
    ):
        pass

    @abstractmethod
    def update_status_by_line_room_id(
        self,
        session,
        line_room_id,
        status,
    ):
        pass

    @abstractmethod
    def update_status_by_id_and_line_room_id(
        self,
        session,
        hanchan_id,
        line_room_id,
        status,
    ):
        pass

    @abstractmethod
    def update_one_converted_score_by_line_room_id(
        self,
        session,
        line_room_id,
        converted_scores,
    ):
        pass
